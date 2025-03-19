from django.contrib.auth.models import AbstractUser
from django.db import models
from rolepermissions.roles import assign_role, clear_roles



class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    email = models.EmailField(unique=True)  # Make email unique
    phone_number = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    
    # Role field for clear role identification
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Assign role permissions on save if it's a new user or role has changed
        self.assign_role()
    
    def assign_role(self):
        """Assign role permissions based on the role field"""
        # Clear existing roles first
        clear_roles(self)
        
        # Assign new role
        if self.role == 'customer':
            assign_role(self, 'customer')
        elif self.role == 'vendor':
            assign_role(self, 'vendor')
        elif self.role == 'staff':
            assign_role(self, 'staff')
        elif self.role == 'manager':
            assign_role(self, 'manager')
        elif self.role == 'admin':
            assign_role(self, 'admin')
