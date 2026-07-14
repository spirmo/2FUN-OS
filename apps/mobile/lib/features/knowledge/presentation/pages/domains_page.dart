import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import 'create_domain_page.dart';

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
    required String titleKey,
  }) {
    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: Icon(
          icon,
          color: Colors.amber,
        ),
        title: Text(
          languageService.text(titleKey),
          style: const TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.w500,
          ),
        ),
        subtitle: Text(
          code,
          style: const TextStyle(
            color: Colors.grey,
            fontSize: 16,
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
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => CreateDomainPage(),
            ),
          );
        },
      ),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          domainTile(
            icon: Icons.menu_book,
            code: "IE",
            titleKey: "domain_ie",
          ),
          domainTile(
            icon: Icons.account_balance,
            code: "IC",
            titleKey: "domain_ic",
          ),
          domainTile(
            icon: Icons.attach_money,
            code: "IEC",
            titleKey: "domain_iec",
          ),
          domainTile(
            icon: Icons.castle,
            code: "AI",
            titleKey: "domain_ai",
          ),
          domainTile(
            icon: Icons.groups,
            code: "SN",
            titleKey: "domain_sn",
          ),
          domainTile(
            icon: Icons.public,
            code: "GK",
            titleKey: "domain_gk",
          ),
          domainTile(
            icon: Icons.apps,
            code: "2FUN",
            titleKey: "domain_2fun",
          ),
        ],
      ),
    );
  }
}
