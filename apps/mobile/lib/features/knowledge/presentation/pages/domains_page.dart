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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(languageService.text("domains")),
        centerTitle: true,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
      body: ListView(
        children: const [
          ListTile(
            leading: Icon(Icons.menu_book),
            title: Text("Islamic Education"),
            subtitle: Text("IE"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.account_balance),
            title: Text("Islamic Culture"),
            subtitle: Text("IC"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.attach_money),
            title: Text("Islamic Economics"),
            subtitle: Text("IEC"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.castle),
            title: Text("Ancient Iran"),
            subtitle: Text("AI"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.groups),
            title: Text("Sociology of Nations"),
            subtitle: Text("SN"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.public),
            title: Text("General Knowledge"),
            subtitle: Text("GK"),
          ),
          Divider(),
          ListTile(
            leading: Icon(Icons.games),
            title: Text("2FUN Platform"),
            subtitle: Text("2FUN"),
          ),
        ],
      ),
    );
  }
}
