import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/database/database_service.dart';
import 'core/diagnostic/diagnostic_initializer.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  print('[BOOT] Before DiagnosticInitializer');
  await DiagnosticInitializer.initialize();
  print('[BOOT] After DiagnosticInitializer');

  print('[BOOT] Before DatabaseService');
  await DatabaseService.instance.database;
  print('[BOOT] After DatabaseService');

  runApp(const TwoFunApp());
}
