import "../config/app_config.dart";
import '../../database/database_service.dart';
import 'providers/recovery/event_bus_diagnostic_recovery.dart';
import 'providers/storage/sqlite_diagnostic_storage.dart';
import 'engine/diagnostic_engine.dart';
import 'publishers/event_bus_diagnostic_publisher.dart';
import 'providers/reporter/local_diagnostic_reporter.dart';
import 'diagnostic_service.dart';
import 'diagnostic_logger.dart';
import 'handlers/flutter_crash_handler.dart';

class DiagnosticInitializer {
  static late DiagnosticService service;

  static Future<void> initialize() async {
    try {
      final logger = DiagnosticLogger();
      final storage = SQLiteDiagnosticStorage(
        databaseService: DatabaseService.instance,
      );
      final reporter = LocalDiagnosticReporter();
      final engine = DiagnosticEngine();

      print("[DIAGNOSTIC] EventBus publisher initialized");

      final publisher = EventBusDiagnosticPublisher(
        apiUrl: diagnosticApiUrl,
      );

      final recovery = EventBusDiagnosticRecovery();

      service = DiagnosticService(
        engine: engine,
        logger: logger,
        storage: storage,
        reporter: reporter,
        publisher: publisher,
        recovery: recovery,
      );

      FlutterCrashHandler(
        service: service,
      ).install();

      await service.record(
        source: "2FUN-OS",
        type: "SYSTEM_START",
        severity: "INFO",
        message: "Diagnostic infrastructure initialized",
        metadata: {
          "layer": "core",
          "mode": "local",
        },
      );

      print(
        "[DIAGNOSTIC] Events: ${service.getEvents().length}",
      );
    } catch (error, stack) {
      print("[DIAGNOSTIC INIT] Initialization failed");
      print(error);
      print(stack);

      // Diagnostic infrastructure must never prevent
      // the application from starting.
    }
  }
}
