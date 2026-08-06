import 'models/diagnostic_event.dart';

abstract class DiagnosticEventPublisher {

  Future<void> publish(
    DiagnosticEvent event,
  );
}
