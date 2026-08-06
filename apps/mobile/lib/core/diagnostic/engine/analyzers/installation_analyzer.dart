import '../../models/diagnostic_event.dart';
import 'base_analyzer.dart';

class InstallationAnalyzer extends BaseDiagnosticAnalyzer {

  @override
  String get name => "Installation Analyzer";


  @override
  Future<DiagnosticEvent> analyze(
    DiagnosticEvent event,
  ) async {

    return event;

  }

}
