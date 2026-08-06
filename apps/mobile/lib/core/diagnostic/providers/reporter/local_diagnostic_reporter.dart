import '../../interfaces/diagnostic_reporter.dart';


class LocalDiagnosticReporter implements DiagnosticReporter {


  final List<Map<String, dynamic>> reports = [];


  @override
  Future<void> report(
    Map<String, dynamic> event,
  ) async {

    reports.add(event);

    print(
      "[DIAGNOSTIC REPORT] $event",
    );

  }

}
