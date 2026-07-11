import 'package:flutter/material.dart';

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
        children: const [
          Card(
            child: ListTile(
              leading: Icon(Icons.public),
              title: Text("Domains"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.folder),
              title: Text("Topics"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.lightbulb),
              title: Text("Concepts"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.label),
              title: Text("Attributes"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.menu_book),
              title: Text("Sources"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.translate),
              title: Text("Translations"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.quiz),
              title: Text("Questions"),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.flag),
              title: Text("Missions"),
            ),
          ),
        ],
      ),
    );
  }
}
