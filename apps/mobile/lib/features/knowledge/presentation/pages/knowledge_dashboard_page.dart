import 'package:flutter/material.dart';

import 'domains_page.dart';

class KnowledgeDashboardPage extends StatelessWidget {
  const KnowledgeDashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Knowledge Injection"),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.public),
              title: const Text("Domains"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const DomainsPage(),
                  ),
                );
              },
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.folder),
              title: const Text("Topics"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.lightbulb),
              title: const Text("Concepts"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.label),
              title: const Text("Attributes"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.menu_book),
              title: const Text("Sources"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.translate),
              title: const Text("Translations"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.quiz),
              title: const Text("Questions"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),

          Card(
            child: ListTile(
              leading: const Icon(Icons.flag),
              title: const Text("Missions"),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {},
            ),
          ),
        ],
      ),
    );
  }
}
