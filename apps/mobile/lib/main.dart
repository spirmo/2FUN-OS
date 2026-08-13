import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/database/database_service.dart';
import 'core/diagnostic/diagnostic_initializer.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await DiagnosticInitializer.initialize();

  await DatabaseService.instance.database;

  runApp(const TwoFunApp());
}
