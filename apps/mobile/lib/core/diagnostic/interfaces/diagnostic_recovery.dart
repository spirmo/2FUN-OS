import '../models/diagnostic_event.dart';

abstract class DiagnosticRecovery {
  Future<bool> canRecover(DiagnosticEvent event);

  Future<void> recover(DiagnosticEvent event);
}
