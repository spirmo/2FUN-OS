import 'package:flutter/widgets.dart';

import 'app/app.dart';
import 'core/database/database_service.dart';

const bool isGovernanceBuild = false;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await DatabaseService.instance.database;

  runApp(const TwoFunApp());
}
