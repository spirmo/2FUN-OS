import 'dart:ui';
import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/database/database_service.dart';
import 'core/diagnostic/diagnostic_initializer.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  DiagnosticInitializer.initialize();
  
  await DiagnosticInitializer.service.record(
    source: "2FUN-OS",
    type: "DIAGNOSTIC_BOOT_TEST",
    severity: "INFO",
    message: "Mobile diagnostic pipeline test",
    metadata: {
      "stage": "startup",
  },
);


FlutterError.onError = (FlutterErrorDetails details) {

  DiagnosticInitializer.service.record(
    source: "2FUN-OS",
    type: "FLUTTER_ERROR",
    severity: "ERROR",
    message: details.exceptionAsString(),
    metadata: {
      "stack": details.stack.toString(),
    },
  );

};


PlatformDispatcher.instance.onError = (error, stack) {

  DiagnosticInitializer.service.record(
    source: "2FUN-OS",
    type: "UNHANDLED_EXCEPTION",
    severity: "CRITICAL",
    message: error.toString(),
    metadata: {
      "stack": stack.toString(),
    },
  );

  return true;

};

  await DatabaseService.instance.database;

  runApp(const TwoFunApp());
}
