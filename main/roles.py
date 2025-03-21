from rolepermissions.roles import AbstractUserRole

class customer(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }

class vendor(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }

class staff(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }

class manager(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }

class admin(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
        'view_own_profile': True,
        'edit_own_profile' : True,
        'manage_staff': True,
        'system_settings': True,
    }