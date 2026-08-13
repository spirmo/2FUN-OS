import 'dart:convert';

import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/database/database_health_service.dart';

class DiagnosticDashboardPage extends StatefulWidget {
  const DiagnosticDashboardPage({
    super.key,
  });

  @override
  State<DiagnosticDashboardPage> createState() =>
      _DiagnosticDashboardPageState();
}

class _DiagnosticDashboardPageState
    extends State<DiagnosticDashboardPage> {

  bool loading = true;
  bool databaseLoading = true;
  List<Map<String, dynamic>> events = [];
  DatabaseHealthReport? databaseHealth;

  @override
  void initState() {
    super.initState();
    _loadEvents();
    _loadDatabaseHealth();
  }

  Future<void> _loadDatabaseHealth() async {
    try {
      final report =
          await DatabaseHealthService.instance.inspect();

      if (!mounted) return;

      setState(() {
        databaseHealth = report;
        databaseLoading = false;
      });
    } catch (_) {
      if (!mounted) return;

      setState(() {
        databaseLoading = false;
      });
    }
  }

  Future<void> _loadEvents() async {
    try {
      final db = await DatabaseService.instance.database;

      final result = await db.query(
        'diagnostic_events',
        orderBy: 'id DESC',
        limit: 100,
      );

      if (!mounted) return;

      setState(() {
        events = result;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        loading = false;
      });
    }
  }

  int _countBySeverity(String severity) {
    return events.where(
      (event) => event['severity'] == severity,
    ).length;
  }

  Color _severityColor(String severity) {
    switch (severity) {
      case 'CRITICAL':
        return Colors.red;
      case 'ERROR':
        return Colors.orange;
      case 'WARNING':
        return Colors.amber;
      case 'INFO':
      default:
        return Colors.green;
    }
  }

  String _metadataText(dynamic metadata) {
    if (metadata == null) return '';

    try {
      final decoded = jsonDecode(metadata.toString());

      if (decoded is Map && decoded.isNotEmpty) {
        return decoded.entries
            .map((e) => '${e.key}: ${e.value}')
            .join('\n');
      }
    } catch (_) {}

    return metadata.toString();
  }

  @override
  Widget build(BuildContext context) {
    final critical = _countBySeverity('CRITICAL');
    final errors = _countBySeverity('ERROR');
    final warnings = _countBySeverity('WARNING');
    final info = _countBySeverity('INFO');

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text(
          'Diagnostic Infrastructure',
        ),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
      ),
      body: loading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : RefreshIndicator(
              onRefresh: _loadEvents,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  const Text(
                    'EV-0018',
                    style: TextStyle(
                      color: Colors.amber,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 8),

                  const Text(
                    'Universal Diagnostic & Recovery Infrastructure',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 15,
                    ),
                  ),

                  const SizedBox(height: 20),

                  Row(
                    children: [
                      Expanded(
                        child: _statCard(
                          'CRITICAL',
                          critical,
                          Colors.red,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _statCard(
                          'ERROR',
                          errors,
                          Colors.orange,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 8),

                  Row(
                    children: [
                      Expanded(
                        child: _statCard(
                          'WARNING',
                          warnings,
                          Colors.amber,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _statCard(
                          'INFO',
                          info,
                          Colors.green,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 24),

                  _databaseHealthSection(),

                  const SizedBox(height: 24),

                  Text(
                    'Recent Events (${events.length})',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 12),

                  if (events.isEmpty)
                    const Card(
                      color: Color(0xFF1E1E1E),
                      child: Padding(
                        padding: EdgeInsets.all(20),
                        child: Text(
                          'No diagnostic events recorded.',
                          style: TextStyle(
                            color: Colors.white70,
                          ),
                        ),
                      ),
                    ),

                  ...events.map(
                    (event) => _eventCard(event),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _databaseHealthSection() {
    if (databaseLoading) {
      return const Card(
        color: Color(0xFF1E1E1E),
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Center(
            child: CircularProgressIndicator(),
          ),
        ),
      );
    }

    final health = databaseHealth;

    if (health == null) {
      return _healthCard(
        title: 'Database Health',
        value: 'UNAVAILABLE',
        details: const [
          'Runtime database inspection failed.',
        ],
        color: Colors.red,
      );
    }

    final schemaColor =
        health.schemaOk ? Colors.green : Colors.red;

    final versionColor =
        health.versionOk ? Colors.green : Colors.red;

    final integrityColor =
        health.integrityOk ? Colors.green : Colors.red;

    final details = <String>[
      'Version: ${health.version}',
      'Expected Version: ${DatabaseHealthService.expectedVersion}',
      'Version Status: ${health.versionOk ? 'OK' : 'MISMATCH'}',
      'Tables: ${health.tables.length}',
      'Expected Tables: ${DatabaseHealthService.expectedTables.length}',
      'Size: ${health.sizeBytes} bytes',
      'Path: ${health.path}',
      'Integrity: ${health.integrityOk ? 'OK' : 'FAILED'}',
      'Schema: ${health.schemaOk ? 'OK' : 'MISMATCH'}',
    ];

    if (health.missingTables.isNotEmpty) {
      details.add(
        'Missing: ${health.missingTables.join(', ')}',
      );
    }

    if (health.extraTables.isNotEmpty) {
      details.add(
        'Extra: ${health.extraTables.join(', ')}',
      );
    }

    return Card(
      color: const Color(0xFF1E1E1E),
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      child: Theme(
        data: Theme.of(context).copyWith(
          dividerColor: Colors.transparent,
        ),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(
            horizontal: 14,
            vertical: 5,
          ),
          childrenPadding: const EdgeInsets.fromLTRB(
            14,
            0,
            14,
            14,
          ),
          iconColor: Colors.white70,
          collapsedIconColor: Colors.white54,
          title: Row(
            children: [
              Container(
                width: 9,
                height: 9,
                decoration: BoxDecoration(
                  color: health.healthy
                      ? Colors.green
                      : Colors.red,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 9),
              const Expanded(
                child: Text(
                  'DATABASE',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              Text(
                health.healthy
                    ? 'HEALTHY'
                    : 'CHECK',
                style: TextStyle(
                  color: health.healthy
                      ? Colors.green
                      : Colors.red,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          subtitle: Padding(
            padding: const EdgeInsets.only(
              left: 18,
              top: 3,
            ),
            child: Text(
              '${health.tables.length} tables • '
              'v${health.version} • '
              '${health.sizeBytes} bytes',
              style: const TextStyle(
                color: Colors.white54,
                fontSize: 10,
              ),
            ),
          ),
          children: [
            const Divider(
              height: 1,
              color: Colors.white10,
            ),
            const SizedBox(height: 10),
            _healthStatusRow(
              'Schema',
              health.schemaOk ? 'OK' : 'MISMATCH',
              schemaColor,
            ),
            _healthStatusRow(
              'Version',
              health.versionOk ? 'OK' : 'MISMATCH',
              versionColor,
            ),
            _healthStatusRow(
              'Integrity',
              health.integrityOk ? 'OK' : 'FAILED',
              integrityColor,
            ),
            const SizedBox(height: 8),
            ...details.map(
              (detail) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text(
                  detail,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 11,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _healthStatusRow(
    String title,
    String value,
    Color color,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        children: [
          Text(
            '$title: ',
            style: const TextStyle(
              color: Colors.white70,
            ),
          ),
          Text(
            value,
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _healthCard({
    required String title,
    required String value,
    required List<String> details,
    required Color color,
  }) {
    return Card(
      color: const Color(0xFF1E1E1E),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Text(
                  value,
                  style: TextStyle(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            ...details.map(
              (detail) => Text(
                detail,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 12,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _statCard(
    String title,
    int count,
    Color color,
  ) {
    final matchingEvents = events
        .where(
          (event) => event['severity']?.toString() == title,
        )
        .toList();

    return Card(
      color: const Color(0xFF1E1E1E),
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      child: Theme(
        data: Theme.of(context).copyWith(
          dividerColor: Colors.transparent,
        ),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(
            horizontal: 14,
            vertical: 5,
          ),
          childrenPadding: const EdgeInsets.fromLTRB(
            14,
            0,
            14,
            12,
          ),
          iconColor: Colors.white70,
          collapsedIconColor: Colors.white54,
          title: Row(
            children: [
              Container(
                width: 9,
                height: 9,
                decoration: BoxDecoration(
                  color: color,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 9),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              Text(
                '$count',
                style: TextStyle(
                  color: color,
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          subtitle: Padding(
            padding: const EdgeInsets.only(
              left: 18,
              top: 3,
            ),
            child: Text(
              count == 0
                  ? 'No events'
                  : '$count diagnostic event${count == 1 ? '' : 's'}',
              style: const TextStyle(
                color: Colors.white54,
                fontSize: 10,
              ),
            ),
          ),
          children: [
            const Divider(
              height: 1,
              color: Colors.white10,
            ),
            const SizedBox(height: 8),
            if (matchingEvents.isEmpty)
              const Align(
                alignment: Alignment.centerLeft,
                child: Padding(
                  padding: EdgeInsets.only(bottom: 4),
                  child: Text(
                    'No diagnostic events recorded.',
                    style: TextStyle(
                      color: Colors.white54,
                      fontSize: 11,
                    ),
                  ),
                ),
              )
            else
              ...matchingEvents.take(10).map(
                (event) => _compactEventDetail(
                  event,
                  color,
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _compactEventDetail(
    Map<String, dynamic> event,
    Color color,
  ) {
    final message =
        event['message']?.toString() ?? '';

    final timestamp =
        event['timestamp']?.toString() ?? '';

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 7),
      padding: const EdgeInsets.all(9),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.035),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 4),
            width: 6,
            height: 6,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                Text(
                  event['type']?.toString() ??
                      'UNKNOWN',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                if (message.isNotEmpty) ...[
                  const SizedBox(height: 3),
                  Text(
                    message,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: Colors.white60,
                      fontSize: 10,
                    ),
                  ),
                ],
                if (timestamp.isNotEmpty) ...[
                  const SizedBox(height: 3),
                  Text(
                    timestamp,
                    style: const TextStyle(
                      color: Colors.white38,
                      fontSize: 9,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _eventCard(
    Map<String, dynamic> event,
  ) {
    final severity =
        event['severity']?.toString() ?? 'INFO';

    final color = _severityColor(severity);

    final message =
        event['message']?.toString() ?? '';

    final metadata =
        _metadataText(event['metadata']);

    return Card(
      color: const Color(0xFF1E1E1E),
      margin: const EdgeInsets.only(bottom: 10),
      child: ExpansionTile(
        iconColor: Colors.white,
        collapsedIconColor: Colors.white70,
        title: Row(
          children: [
            Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                color: color,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                event['type']?.toString() ?? 'UNKNOWN',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
        subtitle: Text(
          '${event['timestamp'] ?? ''}\n$message',
          maxLines: 3,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            color: Colors.white60,
          ),
        ),
        children: [
          if (metadata.isNotEmpty)
            Padding(
              padding: const EdgeInsets.fromLTRB(
                16,
                0,
                16,
                16,
              ),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  metadata,
                  style: const TextStyle(
                    color: Colors.white54,
                    fontSize: 12,
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
