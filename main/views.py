from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections

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
