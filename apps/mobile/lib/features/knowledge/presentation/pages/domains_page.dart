import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';

class DomainsPage extends StatefulWidget {
  const DomainsPage({super.key});

  @override
  State<DomainsPage> createState() => _DomainsPageState();
}

class _DomainsPageState extends State<DomainsPage> {
  final LanguageService languageService = LanguageService();

  @override
  void initState() {
    super.initState();
    _loadLanguage();
  }

  Future<void> _loadLanguage() async {
    final code = await languageService.getLanguage();
    await languageService.load(code);

    if (mounted) {
      setState(() {});
    }
  }

  Widget domainTile({
    required IconData icon,
    required String code,
    required String title,
  }) {
    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: Icon(icon, color: Colors.amber),
        title: Text(
          title,
          style: const TextStyle(color: Colors.white),
        ),
        subtitle: Text(
          code,
          style: const TextStyle(color: Colors.grey),
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
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          domainTile(
            icon: Icons.menu_book,
            code: "IE",
            title: "Islamic Education",
          ),
          domainTile(
            icon: Icons.account_balance,
            code: "IC",
            title: "Islamic Culture",
          ),
          domainTile(
            icon: Icons.attach_money,
            code: "IEC",
            title: "Islamic Economics",
          ),
          domainTile(
            icon: Icons.castle,
            code: "AI",
            title: "Ancient Iran",
          ),
          domainTile(
            icon: Icons.groups,
            code: "SN",
            title: "Sociology of Nations",
          ),
          domainTile(
            icon: Icons.public,
            code: "GK",
            title: "General Knowledge",
          ),
          domainTile(
            icon: Icons.games,
            code: "2FUN",
            title: "2FUN Platform",
          ),
        ],
      ),
    );
  }
}
