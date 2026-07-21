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
    return apiService.evaluateConcept(
      conceptId,
      concept,
    );
  }
}
