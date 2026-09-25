class PermissionEngine:

    def __init__(self, role_manager):
        self.role_manager = role_manager

    def check(
        self,
        role,
        permission,
    ):
        return self.role_manager.has_permission(
            role,
            permission,
        )
