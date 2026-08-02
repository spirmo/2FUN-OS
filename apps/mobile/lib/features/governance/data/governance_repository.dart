import 'governance_api_service.dart';

class GovernanceRepository {

  final GovernanceApiService apiService;


  GovernanceRepository({
    required this.apiService,
  });



  Map<String, dynamic> evaluateConcept(
    int conceptId,
    Map<String, dynamic> concept,
  ) {

    final result =
        apiService.evaluateConcept(
      conceptId,
      concept,
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
          result["validation_time"],

      "completeness":
          result["completeness"],
    };
  }
}
