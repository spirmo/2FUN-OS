import 'engine/diagnostic_engine.dart';
import 'models/diagnostic_event.dart';
import 'models/crash_report.dart';
import 'diagnostic_logger.dart';
import 'interfaces/diagnostic_storage.dart';
import 'interfaces/diagnostic_reporter.dart';
import 'interfaces/diagnostic_event_publisher.dart';
import 'interfaces/diagnostic_recovery.dart';

class DiagnosticService {
  final DiagnosticEngine engine;
  final DiagnosticLogger logger;
  final DiagnosticStorage? storage;
  final DiagnosticReporter? reporter;
  final DiagnosticEventPublisher? publisher;
  final DiagnosticRecovery? recovery;

  DiagnosticService({
    required this.engine,
    required this.logger,
    this.storage,
    this.reporter,
    this.publisher,
    this.recovery,
  });

  Future<void> record({
    required String source,
    required String type,
    required String severity,
    required String message,
    Map<String, dynamic>? metadata,
  }) async {
    final event = DiagnosticEvent(
      id: _generateErrorId(),
      timestamp: DateTime.now(),
      source: source,
      type: type,
      severity: severity,
      message: message,
      metadata: metadata,
    );

    final processedEvent = await engine.process(event);

    logger.log(processedEvent);

    await storage?.save(
      processedEvent.toMap(),
    );

    if (publisher != null) {
      await publisher!.publish(processedEvent);
    }

    await reporter?.report(
      processedEvent.toMap(),
    );

    if (await recovery?.canRecover(processedEvent) ?? false) {
      await recovery!.recover(processedEvent);
    }
  }

  Future<void> recordCrash({
    required Object exception,
    required StackTrace stackTrace,
    String? appVersion,
    String? buildNumber,
    String? deviceModel,
    String? androidVersion,
    String? currentPage,
    String? userRole,
    String? lastEvent,
  }) async {
    final errorId = _generateErrorId();
    final timestamp = DateTime.now();

    final crashReport = CrashReport(
      errorId: errorId,
      timestamp: timestamp,
      appVersion: appVersion,
      buildNumber: buildNumber,
      deviceModel: deviceModel,
      androidVersion: androidVersion,
      currentPage: currentPage,
      userRole: userRole,
      lastEvent: lastEvent,
      exception: exception.toString(),
      stackTrace: stackTrace.toString(),
    );

    await record(
      source: "2FUN-OS",
      type: "APP_CRASHED",
      severity: "CRITICAL",
      message: exception.toString(),
      metadata: crashReport.toMap(),
    );
  }

  String _generateErrorId() {
    return "ERR-${DateTime.now().microsecondsSinceEpoch}";
  }

  List<DiagnosticEvent> getEvents() {
    return logger.events;
  }

  void clear() {
    logger.clear();
  }
}
