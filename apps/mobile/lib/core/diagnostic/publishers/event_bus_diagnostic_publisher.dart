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

    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({

        "source": event.source,

        "event_type": event.type,

        "target": "diagnostic",

        "value": {
          "severity": event.severity,
          "message": event.message,
          "metadata": event.metadata,
        },

      }),
    );


    if (response.statusCode != 200) {
      throw Exception(
        "Diagnostic EventBus publish failed: ${response.body}",
      );
    }
  }
}
