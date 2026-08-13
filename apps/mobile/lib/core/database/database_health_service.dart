import 'dart:io';

import 'package:sqflite/sqflite.dart';

import 'database_service.dart';

class DatabaseHealthReport {
  final String path;
  final int version;
  final int sizeBytes;

  final List<String> tables;
  final List<String> missingTables;
  final List<String> extraTables;

  final bool integrityOk;

  final String? error;

  DatabaseHealthReport({
    required this.path,
    required this.version,
    required this.sizeBytes,
    required this.tables,
    required this.missingTables,
    required this.extraTables,
    required this.integrityOk,
    this.error,
  });

  bool get schemaOk => missingTables.isEmpty;
  bool get versionOk =>
      version == DatabaseHealthService.expectedVersion;

  bool get healthy =>
      schemaOk && versionOk && integrityOk && error == null;

  Map<String, dynamic> toMap() {
    return {
      'path': path,
      'version': version,
      'size_bytes': sizeBytes,
      'tables': tables,
      'missing_tables': missingTables,
      'extra_tables': extraTables,
      'integrity_ok': integrityOk,
      'schema_ok': schemaOk,
      'version_ok': versionOk,
      'healthy': healthy,
      'error': error,
    };
  }
}

class DatabaseHealthService {
  DatabaseHealthService._();

  static final DatabaseHealthService instance =
      DatabaseHealthService._();

  static const int expectedVersion = 9;

  static const List<String> expectedTables = [
    'domains',
    'topics',
    'concepts',
    'attributes',
    'sources',
    'translations',
    'questions',
    'missions',
    'concept_items',
    'concept_system',
    'concept_extensions',
    'roles',
    'users',
    'diagnostic_events',
  ];

  Future<DatabaseHealthReport> inspect() async {
    try {
      final db = await DatabaseService.instance.database;

      final path =
          await DatabaseService.instance.getDatabasePath();

      final file = File(path);

      final sizeBytes =
          await file.exists() ? await file.length() : 0;

      final versionResult =
          await db.rawQuery('PRAGMA user_version');

      final version =
          versionResult.isNotEmpty
              ? (versionResult.first.values.first as int? ?? 0)
              : 0;

      final tableResult = await db.rawQuery(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name",
      );

      final tables = tableResult
          .map(
            (row) => row['name']?.toString() ?? '',
          )
          .where(
            (name) => name.isNotEmpty,
          )
          .toList();

      final missingTables = expectedTables
          .where(
            (table) => !tables.contains(table),
          )
          .toList();

      final extraTables = tables
          .where(
            (table) => !expectedTables.contains(table),
          )
          .toList();

      final integrityResult =
          await db.rawQuery(
        'PRAGMA integrity_check',
      );

      final integrityOk =
          integrityResult.isNotEmpty &&
          integrityResult.first.values.first
                  ?.toString()
                  .toLowerCase() ==
              'ok';

      return DatabaseHealthReport(
        path: path,
        version: version,
        sizeBytes: sizeBytes,
        tables: tables,
        missingTables: missingTables,
        extraTables: extraTables,
        integrityOk: integrityOk,
      );
    } catch (error) {
      return DatabaseHealthReport(
        path: 'UNKNOWN',
        version: 0,
        sizeBytes: 0,
        tables: const [],
        missingTables: List<String>.from(
          expectedTables,
        ),
        extraTables: const [],
        integrityOk: false,
        error: error.toString(),
      );
    }
  }
}
