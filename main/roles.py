from rolepermissions.roles import AbstractUserRole

class Customer(AbstractUserRole):
    available_permissions = {
        'cust_permission': True,
    }

class Vendor(AbstractUserRole):
    available_permissions = {
        'vendor_permission': True,
    }

class Staff(AbstractUserRole):
    available_permissions = {
        'staff_permission': True,
    }

class Manager(AbstractUserRole):
    available_permissions = {
        'manager_permission': True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
    }