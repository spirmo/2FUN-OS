from .role_manager import RoleManager
from .permission_engine import PermissionEngine


class IdentityService:

    def __init__(self):

        self.role_manager = RoleManager()

        self.permission_engine = PermissionEngine(
            self.role_manager,
        )

    def register_role(
        self,
        role,
        permissions,
    ):

        self.role_manager.register_role(
            role,
            permissions,
        )

    def can(
        self,
        role,
        permission,
    ):

        return self.permission_engine.check(
            role,
            permission,
        )
