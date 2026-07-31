import 'dart:io';

import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

class DatabaseExportService {
  static Future<String> exportDatabase() async {
    final dbDir = await getDatabasesPath();

    final dbFile = File(join(dbDir, '2fun.db'));

    final downloadDir = await getExternalStorageDirectory();

    final exportFile = File(
      join(downloadDir!.path, '2fun_export.db'),
    );

    await exportFile.writeAsBytes(
      await dbFile.readAsBytes(),
    );

    return exportFile.path;
  }
}
