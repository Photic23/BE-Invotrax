from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer, RegisterSerializer
from .permissions import HasRolePermission
from rolepermissions.permissions import revoke_permission, grant_permission

User = get_user_model()

def test_db_connection(request):
    try:
        # Get the default database connection
        conn = connections['default']
        
        # Try to connect
        conn.ensure_connection()
        
        # Execute a simple query
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        return JsonResponse({
            "status": "success",
            "message": "Successfully connected to Supabase PostgreSQL"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error", 
            "message": str(e)
        }, status=500)
# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not (email):
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Try to find user by email
            user_obj = User.objects.get(email=email)
            # Try to authenticate with both email and username
            user = authenticate(request, email=email, password=password)
            if not user:
                # If email auth fails, try username auth
                user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user:
            refresh = RefreshToken.for_user(user)
            
            # Add custom claims to the token
            refresh['role'] = user.role  # Add role to the refresh token
            refresh['name'] = user.username
            refresh.access_token['role'] = user.role  # Add role to the access token
            refresh.access_token['name'] = user.username  # Add role to the access token
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    required_permission = 'view_own_profile'
    permission_classes = [HasRolePermission]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        # Check if user has permission to edit their profile
        # if not has_permission(request.user, 'edit_own_profile'):
        #     return Response(
        #         {"error": "You don't have permission to edit your profile"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
            
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            # Check if role is being changed
            if 'role' in serializer.validated_data and request.user.role != serializer.validated_data['role']:
                # Only admins can change roles
                if not has_role(request.user, 'admin'):
                    return Response(
                        {"error": "Only administrators can change user roles"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin views for user management
class UserManagementView(APIView):
    required_permission = 'manage_staff'
    permission_classes = [HasRolePermission]
    
    def get(self, request):
        # List all users - filtered by role if specified
        role = request.query_params.get('role', None)
        
        if role:
            users = User.objects.filter(role=role)
        else:
            users = User.objects.all()
            
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Create a new user with role
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, user_id):
        # Update user role and permissions
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if changing manager/admin (requires admin role)
        new_role = request.data.get('role')
        if new_role in ['manager', 'admin'] and not has_role(request.user, 'admin'):
            return Response(
                {"error": "Only administrators can assign manager or admin roles"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        # Delete a user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if deleting manager/admin (requires admin role)
        if user.role in ['manager', 'admin'] and not has_role(request.user, 'admin'):
            return Response(
                {"error": "Only administrators can delete managers or admins"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Custom permissions management
class CustomPermissionView(APIView):
    required_permission = 'system_settings'
    permission_classes = [HasRolePermission]
    
    def post(self, request, user_id):
        # Grant custom permission to a user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        permission_name = request.data.get('permission')
        grant_status = request.data.get('grant', True)
        
        if not permission_name:
            return Response({"error": "Permission name is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if grant_status:
            grant_permission(user, permission_name)
        else:
            revoke_permission(user, permission_name)
            
        return Response({"status": "Permission updated"})

def test():
    print("test")
