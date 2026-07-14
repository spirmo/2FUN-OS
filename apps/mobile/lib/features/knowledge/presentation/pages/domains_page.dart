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

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    final code = await languageService.getLanguage();
    await languageService.load(code);
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
    final lang = languageService.text("app_name");

    if (lang == "توفان") {
      return domain["name_fa"] ?? "";
    }

    if (lang == "2FUN") {
      final language = languageService.text("continue_guest");

      if (language == "الدخول كضيف") {
        return domain["name_ar"] ?? "";
      }

      return domain["name_en"] ?? "";
    }

    return domain["name_en"] ?? "";
  }

  Widget domainTile(Map<String, dynamic> domain) {
    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: const Icon(
          Icons.folder,
          color: Colors.amber,
        ),
        title: Text(
          _domainName(domain),
          style: const TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.w500,
          ),
        ),
        subtitle: Text(
          domain["code"],
          style: const TextStyle(
            color: Colors.grey,
          ),
        ),
        trailing: const Icon(
          Icons.chevron_right,
          color: Colors.amber,
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
            setState(() {});
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
