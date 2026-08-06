class DiagnosticEvent {

  final String id;

  final DateTime timestamp;

  final String source;

  final String type;

  final String severity;

  final String message;

  final Map<String, dynamic>? metadata;


  DiagnosticEvent({

    required this.id,

    required this.timestamp,

    required this.source,

    required this.type,

    required this.severity,

    required this.message,

    this.metadata,

  });


  Map<String, dynamic> toMap() {

    return {

      "id": id,

      "timestamp": timestamp.toIso8601String(),

      "source": source,

      "type": type,

      "severity": severity,

      "message": message,

      "metadata": metadata ?? {},

    };

  }


  factory DiagnosticEvent.fromMap(
    Map<String, dynamic> map,
  ) {

    return DiagnosticEvent(

      id: map["id"],

      timestamp: DateTime.parse(
        map["timestamp"],
      ),

      source: map["source"],

      type: map["type"],

      severity: map["severity"],

      message: map["message"],

      metadata: map["metadata"],

    );

  }

}
