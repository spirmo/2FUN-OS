import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import 'create_domain_page.dart';

class DomainsPage extends StatefulWidget {
  const DomainsPage({super.key});

  @override
  State<DomainsPage> createState() => _DomainsPageState();
}

class _DomainsPageState extends State<DomainsPage> {
  final LanguageService languageService = LanguageService();

  List<Map<String, dynamic>> domains = [];
  String currentLanguage = 'fa';

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    currentLanguage = await languageService.getLanguage();
    await languageService.load(currentLanguage);
    await _loadDomains();

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _loadDomains() async {
    final db = await DatabaseService.instance.database;

    domains = await db.query(
      'domains',
      orderBy: 'id ASC',
    );
  }

  String _domainName(Map<String, dynamic> domain) {
    switch (currentLanguage) {
      case 'fa':
        return (domain['name_fa'] ?? '').toString();
      case 'ar':
        return (domain['name_ar'] ?? '').toString();
      default:
        return (domain['name_en'] ?? '').toString();
    }
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'APPROVED':
        return Colors.amber;
      case 'REJECTED':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData _statusIcon(String status) {
    switch (status) {
      case 'APPROVED':
        return Icons.verified;
      case 'REJECTED':
        return Icons.cancel;
      default:
        return Icons.schedule;
    }
  }

  Widget domainTile(Map<String, dynamic> domain) {
    final status = (domain['status'] ?? 'PENDING').toString();

    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: Icon(
          _statusIcon(status),
          color: _statusColor(status),
        ),
        title: Text(
          _domainName(domain),
          style: TextStyle(
            color: _statusColor(status),
            fontSize: 20,
            fontWeight: FontWeight.w500,
          ),
        ),
        subtitle: Text(
          domain['code'].toString(),
          style: const TextStyle(
            color: Colors.grey,
          ),
        ),
        trailing: Icon(
          Icons.chevron_right,
          color: _statusColor(status),
        ),
        onTap: () {},
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        centerTitle: true,
        title: Text(
          languageService.text("domains"),
          style: const TextStyle(
            color: Colors.amber,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.amber,
        foregroundColor: Colors.black,
        child: const Icon(Icons.add),
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => CreateDomainPage(),
            ),
          );

          if (result == true) {
            await _loadDomains();

            if (mounted) {
              setState(() {});
            }
          }
        },
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: domains.length,
        itemBuilder: (context, index) {
          return domainTile(domains[index]);
        },
      ),
    );
  }
}
