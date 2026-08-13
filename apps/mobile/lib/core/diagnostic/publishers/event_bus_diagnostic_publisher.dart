import 'dart:convert';

import 'package:http/http.dart' as http;

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
    if (apiUrl.trim().isEmpty) {
      print("[DIAGNOSTIC] API URL is empty; event kept local.");
      return;
    }

    try {
      final response = await http
          .post(
            Uri.parse(
              "${apiUrl.replaceAll(RegExp(r'/$'), '')}/diagnostic/crash",
            ),
            headers: {
              "Content-Type": "application/json",
            },
            body: jsonEncode(event.toMap()),
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode >= 200 &&
          response.statusCode < 300) {
        print(
          "[DIAGNOSTIC] Event published successfully: "
          "${response.statusCode}",
        );
      } else {
        print(
          "[DIAGNOSTIC] Event publish failed: "
          "${response.statusCode}",
        );
      }
    } catch (error) {
      print(
        "[DIAGNOSTIC] Event publish error: $error",
      );

      // Diagnostic publishing must never
      // prevent the application from running.
    }
  }
}
