import 'models/diagnostic_event.dart';

class DiagnosticLogger {

  final List<DiagnosticEvent> _events = [];

  void log(DiagnosticEvent event) {
    _events.add(event);
  }

  List<DiagnosticEvent> get events {
    return List.unmodifiable(_events);
  }

  void clear() {
    _events.clear();
  }
}
