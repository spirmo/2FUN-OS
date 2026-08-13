import 'dart:ui';
import 'package:flutter/foundation.dart';

import '../diagnostic_service.dart';

class FlutterCrashHandler {
  final DiagnosticService service;

  FlutterCrashHandler({
    required this.service,
  });

  void install() {
    FlutterError.onError = (FlutterErrorDetails details) {
      final stackTrace =
          details.stack ?? StackTrace.current;

      _recordSafely(
        exception: details.exception,
        stackTrace: stackTrace,
        source: "FlutterError.onError",
      );
    };

    PlatformDispatcher.instance.onError = (
      Object error,
      StackTrace stack,
    ) {
      _recordSafely(
        exception: error,
        stackTrace: stack,
        source: "PlatformDispatcher.onError",
      );

      return true;
    };
  }

  Future<void> _recordSafely({
    required Object exception,
    required StackTrace stackTrace,
    required String source,
  }) async {
    try {
      await service.recordCrash(
        exception: exception,
        stackTrace: stackTrace,
      );
    } catch (diagnosticError, diagnosticStack) {
      print(
        "[DIAGNOSTIC FALLBACK] Failed to record crash from $source",
      );
      print(diagnosticError);
      print(diagnosticStack);
    }
  }
}
