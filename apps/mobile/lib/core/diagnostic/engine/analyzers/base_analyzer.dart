import '../../models/diagnostic_event.dart';

abstract class BaseDiagnosticAnalyzer {

  String get name;

  Future<DiagnosticEvent> analyze(
    DiagnosticEvent event,
  );

}
