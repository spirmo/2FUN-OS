class GovernanceController {
  const GovernanceController();

  Map<String, dynamic> submitConcept({
    required int conceptId,
    required Map<String, dynamic> concept,
  }) {
    final valid =
        (concept["source"] != null &&
         concept["evidence"] != null &&
         concept["definition"] != null);

    return {
      "entity_type": "concept",
      "entity_id": conceptId,
      "approved": valid,
      "status": valid ? "APPROVED" : "REJECTED",

      // اتصال به معماری دسترسی توفان
      "required_role": "Validator",
      "required_permission": "concept_approve",
    };
  }

  List<String> permissionsForRole(String role) {
    switch (role) {
      case "Founder":
        return [
          "concept_approve",
          "user_manage",
          "content_review",
          "audit_reports",
        ];

      case "System Overseer":
        return [
          "concept_approve",
          "user_manage",
          "content_review",
          "audit_reports",
        ];

      case "Rule Approver":
        return [
          "concept_approve",
        ];

      case "Validator":
        return [
          "concept_approve",
        ];

      case "Moderator":
        return [
          "content_review",
        ];

      case "Auditor":
        return [
          "audit_reports",
        ];

      default:
        return [];
    }
  }
}
