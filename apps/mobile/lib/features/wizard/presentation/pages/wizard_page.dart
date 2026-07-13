import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';

class WizardPage extends StatefulWidget {
  const WizardPage({super.key});

  @override
  State<WizardPage> createState() => _WizardPageState();
}

class _WizardPageState extends State<WizardPage> {
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
        title: Text(languageService.text("concept_package_wizard")),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const ListTile(
            leading: CircleAvatar(child: Text('1')),
            title: Text('Canonical Name'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('2')),
            title: Text('Short Description'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('3')),
            title: Text('Definitions'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('4')),
            title: Text('Evidence'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('5')),
            title: Text('Aliases'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('6')),
            title: Text('Relationships'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('7')),
            title: Text('Review'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('8')),
            title: Text('Save Draft'),
          ),
          const ListTile(
            leading: CircleAvatar(child: Text('9')),
            title: Text('Submit'),
          ),
        ],
      ),
    );
  }
}
