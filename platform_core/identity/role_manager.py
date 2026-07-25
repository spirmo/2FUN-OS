class RoleManager:

    def __init__(self):
        self.roles = {}
        self._load_default_roles()


    def _load_default_roles(self):

        # =========================
        # BASIC USERS
        # =========================

        self.register_role(
            "Newbie",
            []
        )

        self.register_role(
            "Active User",
            [
                "mission_create",
            ]
        )

        self.register_role(
            "Contributor",
            [
                "mission_create",
                "mission_assign",
            ]
        )


        # =========================
        # ADVANCED USERS
        # =========================

        self.register_role(
            "Specialist",
            [
                "mission_create",
                "mission_assign",
                "mission_validate",
            ]
        )

        self.register_role(
            "Strategist",
            [
                "mission_create",
                "mission_assign",
                "mission_validate",
            ]
        )

        self.register_role(
            "Veteran",
            [
                "mission_create",
                "mission_assign",
                "mission_validate",
            ]
        )


        # =========================
        # COLONY ROLES
        # =========================

        self.register_role(
            "Member",
            [
                "basic_interaction",
                "participation",
            ]
        )

        self.register_role(
            "Coordinator",
            [
                "mission_assign",
                "community_help",
            ]
        )

        self.register_role(
            "Sub-Leader",
            [
                "mission_assign",
                "colony_control",
            ]
        )

        self.register_role(
            "Colony Leader",
            [
                "colony_control",
                "user_manage",
            ]
        )


        # =========================
        # SYSTEM ROLES
        # =========================

        self.register_role(
            "Analyst",
            [
                "rule_view",
            ]
        )

        self.register_role(
            "Moderator",
            [
                "content_review",
                "mission_validate",
            ]
        )

        self.register_role(
            "Validator",
            [
                "concept_approve",
                "mission_validate",
            ]
        )

        self.register_role(
            "Auditor",
            [
                "audit_reports",
                "rule_view",
            ]
        )


        # =========================
        # GOVERNANCE ROLES
        # =========================

        self.register_role(
            "Council Member",
            [
                "governance_vote",
                "rule_view",
            ]
        )

        self.register_role(
            "System Overseer",
            [
                "all_access",
                "governance_vote",
                "user_manage",
                "content_review",
                "audit_reports",
            ]
        )

        self.register_role(
            "Rule Approver",
            [
                "rule_view",
                "reward_modify",
                "economy_control",
                "user_manage",
                "concept_approve",
            ]
        )


    def register_role(
        self,
        role_name,
        permissions,
    ):
        self.roles[role_name] = permissions


    def get_permissions(
        self,
        role_name,
    ):
        return self.roles.get(
            role_name,
            []
        )


    def has_permission(
        self,
        role_name,
        permission,
    ):
        return permission in self.get_permissions(
            role_name
        )
