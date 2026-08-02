import '../domain/governance_controller.dart';

class GovernanceApiService {

  final GovernanceController controller;


  GovernanceApiService({
    required this.controller,
  });



  Map<String, dynamic> evaluateConcept(
    int conceptId,
    Map<String, dynamic> concept,
  ) {

    final result =
        controller.submitConcept(
      conceptId: conceptId,
      concept: concept,
    );


    return {
      "entity_type":
          result["entity_type"],

      "entity_id":
          result["entity_id"],

      "approved":
          result["approved"],

      "status":
          result["status"],

      "required_role":
          result["required_role"],

      "required_permission":
          result["required_permission"],

      "validation_time":
          DateTime.now()
              .toIso8601String(),

      "completeness":
          concept["completeness"] ?? 0,

    };
  }
}
