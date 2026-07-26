class PermissionService {

  static bool can(
    String role,
    String permission,
  ) {

    final permissions = {

      "Newbie": [],

      "Active User": [
        "mission_create",
      ],

      "Contributor": [
        "mission_create",
        "mission_assign",
      ],

      "Specialist": [
        "mission_create",
        "mission_assign",
        "mission_validate",
      ],

      "Strategist": [
        "mission_create",
        "mission_assign",
        "mission_validate",
      ],

      "Veteran": [
        "mission_create",
        "mission_assign",
        "mission_validate",
      ],

      "Member": [
        "basic_interaction",
        "participation",
      ],

      "Coordinator": [
        "mission_assign",
        "community_help",
      ],

      "Sub-Leader": [
        "mission_assign",
        "colony_control",
      ],

      "Colony Leader": [
        "colony_control",
        "user_manage",
      ],

      "Analyst": [
        "rule_view",
      ],

      "Moderator": [
        "content_review",
        "mission_validate",
      ],

      "VALIDATOR": [
        "concept_approve",
        "mission_validate",
      ],

      "Auditor": [
        "audit_reports",
        "rule_view",
      ],

      "Council Member": [
        "governance_vote",
        "rule_view",
      ],

      "System Overseer": [
        "all_access",
        "governance_vote",
        "user_manage",
        "content_review",
        "audit_reports",
      ],

      "Rule Approver": [
        "rule_view",
        "reward_modify",
        "economy_control",
        "user_manage",
        "concept_approve",
      ],

    };


    return permissions[role]
        ?.contains(permission) ??
        false;
  }
}
