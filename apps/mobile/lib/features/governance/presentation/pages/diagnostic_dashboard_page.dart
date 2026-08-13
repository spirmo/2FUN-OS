import 'dart:convert';

import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';

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
  List<Map<String, dynamic>> events = [];

  @override
  void initState() {
    super.initState();
    _loadEvents();
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

  Widget _statCard(
    String title,
    int count,
    Color color,
  ) {
    return Card(
      color: const Color(0xFF1E1E1E),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              '$count',
              style: TextStyle(
                color: color,
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              title,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 12,
              ),
            ),
          ],
        ),
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
