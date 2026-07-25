class RoleManager:

    def __init__(self):
    self.roles = {}
    self._load_default_roles()


    def _load_default_roles(self):

    self.register_role("Newbie", [])

    self.register_role("Active User", [
        "mission_create",
    ])

    self.register_role("Contributor", [
        "mission_create",
        "mission_assign",
    ])

    self.register_role("Specialist", [
        "mission_create",
        "mission_assign",
        "mission_validate",
    ])

    self.register_role("Moderator", [
        "mission_validate",
    ])

    self.register_role("Auditor", [
        "rule_view",
    ])

    self.register_role("Rule Approver", [
        "rule_view",
        "reward_modify",
        "economy_control",
        "user_manage",
    ])
    def register_role(self, role_name, permissions):
        self.roles[role_name] = permissions

    def get_permissions(self, role_name):
        return self.roles.get(role_name, [])

    def has_permission(self, role_name, permission):
        return permission in self.get_permissions(role_name)
