class RoleManager:

    def __init__(self):
        self.roles = {}

    def register_role(self, role_name, permissions):
        self.roles[role_name] = permissions

    def get_permissions(self, role_name):
        return self.roles.get(role_name, [])

    def has_permission(self, role_name, permission):
        return permission in self.get_permissions(role_name)
