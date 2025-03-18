from rolepermissions.roles import AbstractUserRole

class Customer(AbstractUserRole):
    available_permissions = {
        'cust_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
    }

class Vendor(AbstractUserRole):
    available_permissions = {
        'vendor_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
    }

class Staff(AbstractUserRole):
    available_permissions = {
        'staff_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
    }

class Manager(AbstractUserRole):
    available_permissions = {
        'manager_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }