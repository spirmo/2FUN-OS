class PermissionService {

  static bool can(
    String role,
    String permission,
  ) {

    final permissions = {

      "ADMIN": [
        "concept_approve",
        "user_manage",
        "content_review",
        "audit_reports",
      ],

      "GOVERNOR": [
        "concept_approve",
      ],

      "VALIDATOR": [
        "concept_approve",
      ],

      "MODERATOR": [
        "content_review",
      ],

      "AUDITOR": [
        "audit_reports",
      ],

      "USER": [],

    };


    return permissions[role]
        ?.contains(permission) ??
        false;
  }
}
