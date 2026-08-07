import '../models/diagnostic_event.dart';
import '../interfaces/diagnostic_event_publisher.dart';

class EventBusDiagnosticPublisher
    implements DiagnosticEventPublisher {

  final String apiUrl;

  EventBusDiagnosticPublisher({
    required this.apiUrl,
  });

  @override
  Future<void> publish(
    DiagnosticEvent event,
  ) async {

    print("[DIAGNOSTIC EVENT]");
    print(event.toMap());

  }
}
