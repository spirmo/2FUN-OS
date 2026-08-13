class CrashReport {
  final String errorId;
  final DateTime timestamp;

  final String? appVersion;
  final String? buildNumber;
  final String? deviceModel;
  final String? androidVersion;

  final String? currentPage;
  final String? userRole;
  final String? lastEvent;

  final String exception;
  final String stackTrace;

  CrashReport({
    required this.errorId,
    required this.timestamp,
    required this.exception,
    required this.stackTrace,
    this.appVersion,
    this.buildNumber,
    this.deviceModel,
    this.androidVersion,
    this.currentPage,
    this.userRole,
    this.lastEvent,
  });

  Map<String, dynamic> toMap() {
    return {
      "errorId": errorId,
      "timestamp": timestamp.toIso8601String(),
      "appVersion": appVersion,
      "buildNumber": buildNumber,
      "deviceModel": deviceModel,
      "androidVersion": androidVersion,
      "currentPage": currentPage,
      "userRole": userRole,
      "lastEvent": lastEvent,
      "exception": exception,
      "stackTrace": stackTrace,
    };
  }

  factory CrashReport.fromMap(Map<String, dynamic> map) {
    return CrashReport(
      errorId: map["errorId"]?.toString() ?? "",
      timestamp: DateTime.parse(map["timestamp"].toString()),
      appVersion: map["appVersion"]?.toString(),
      buildNumber: map["buildNumber"]?.toString(),
      deviceModel: map["deviceModel"]?.toString(),
      androidVersion: map["androidVersion"]?.toString(),
      currentPage: map["currentPage"]?.toString(),
      userRole: map["userRole"]?.toString(),
      lastEvent: map["lastEvent"]?.toString(),
      exception: map["exception"]?.toString() ?? "",
      stackTrace: map["stackTrace"]?.toString() ?? "",
    );
  }
}
