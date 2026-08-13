import 'dart:convert';

import 'package:sqflite/sqflite.dart';

import '../../interfaces/diagnostic_storage.dart';
import '../../../database/database_service.dart';

class SQLiteDiagnosticStorage implements DiagnosticStorage {
  final DatabaseService databaseService;

  SQLiteDiagnosticStorage({
    required this.databaseService,
  });

  @override
  Future<void> save(Map<String, dynamic> event) async {
    final db = await databaseService.database;

    await db.insert(
      'diagnostic_events',
      {
        'event_id': event['id']?.toString() ?? '',
        'timestamp': event['timestamp']?.toString() ??
            DateTime.now().toIso8601String(),
        'source': event['source']?.toString() ?? '',
        'type': event['type']?.toString() ?? '',
        'severity': event['severity']?.toString() ?? '',
        'message': event['message']?.toString(),
        'metadata': jsonEncode(event['metadata'] ?? {}),
        'created_at': DateTime.now().toIso8601String(),
      },
    );
  }

  @override
  Future<List<Map<String, dynamic>>> load() async {
    final db = await databaseService.database;

    return await db.query(
      'diagnostic_events',
      orderBy: 'id ASC',
    );
  }

  @override
  Future<void> clear() async {
    final db = await databaseService.database;

    await db.delete('diagnostic_events');
  }
}
