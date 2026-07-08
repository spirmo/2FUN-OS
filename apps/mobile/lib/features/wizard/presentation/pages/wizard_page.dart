import 'package:flutter/material.dart';

class WizardPage extends StatelessWidget {
  const WizardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Concept Package Wizard'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          ListTile(
            leading: CircleAvatar(child: Text('1')),
            title: Text('Canonical Name'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('2')),
            title: Text('Short Description'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('3')),
            title: Text('Definitions'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('4')),
            title: Text('Evidence'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('5')),
            title: Text('Aliases'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('6')),
            title: Text('Relationships'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('7')),
            title: Text('Review'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('8')),
            title: Text('Save Draft'),
          ),
          ListTile(
            leading: CircleAvatar(child: Text('9')),
            title: Text('Submit'),
          ),
        ],
      ),
    );
  }
}
