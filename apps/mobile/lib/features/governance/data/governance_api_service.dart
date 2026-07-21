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
    return controller.submitConcept(
      conceptId,
      concept,
    );
  }
}
