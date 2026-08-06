import '../models/diagnostic_event.dart';
import 'analyzers/base_analyzer.dart';
import 'analyzers/installation_analyzer.dart';


class DiagnosticEngine {


  final List<BaseDiagnosticAnalyzer> analyzers = [

    InstallationAnalyzer(),

  ];



  Future<DiagnosticEvent> process(
    DiagnosticEvent event,
  ) async {


    DiagnosticEvent processedEvent = event;


    for (final analyzer in analyzers) {

      processedEvent =
          await analyzer.analyze(
            processedEvent,
          );

    }


    return processedEvent;

  }

}
