class DiagnosticAnalysis {

  final String analyzer;

  final String category;

  final String? rootCause;

  final String severity;

  final String? recommendation;

  final bool recoverable;


  DiagnosticAnalysis({

    required this.analyzer,

    required this.category,

    this.rootCause,

    required this.severity,

    this.recommendation,

    this.recoverable = false,

  });


  Map<String, dynamic> toMap(){

    return {

      "analyzer": analyzer,

      "category": category,

      "rootCause": rootCause,

      "severity": severity,

      "recommendation": recommendation,

      "recoverable": recoverable,

    };

  }

}
