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
    };
  }
}
