const bool isGovernanceBuild =
    bool.fromEnvironment('GOVERNANCE_BUILD', defaultValue: false);


const String diagnosticApiUrl =
    String.fromEnvironment(
      'DIAGNOSTIC_API_URL',
      defaultValue: 'http://127.0.0.1:8000/events/',
    );
