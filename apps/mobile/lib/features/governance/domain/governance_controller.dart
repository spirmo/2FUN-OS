import 'permission_service.dart';

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
      "status": valid
          ? "APPROVED"
          : "REJECTED",

      "required_role": "Validator",
      "required_permission": "concept_approve",
    };
  }

  List<String> permissionsForRole(String role) {

  final allPermissions = [
    "concept_approve",
  ];  

  /*List<String> permissionsForRole(String role) {

    final allPermissions = [

      "mission_create",
      "mission_assign",
      "mission_validate",
      "basic_interaction",
      "participation",
      "community_help",
      "colony_control",
      "user_manage",
      "rule_view",
      "content_review",
      "concept_approve",
      "audit_reports",
      "governance_vote",
      "reward_modify",
      "economy_control",
      "all_access",

    ];*/

    return allPermissions
        .where(
          (permission) =>
              PermissionService.can(
                role,
                permission,
              ),
        )
        .toList();
  }
}
