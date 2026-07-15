import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';

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

  Widget stepTile(String number, String title) {
    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 12,
          vertical: 2,
        ),
        leading: CircleAvatar(
          radius: 14,
          backgroundColor: Colors.amber,
          child: Text(
            number,
            style: const TextStyle(
              color: Colors.black,
              fontWeight: FontWeight.bold,
              fontSize: 12,
            ),
          ),
        ),
        trailing: const Icon(
          Icons.chevron_right,
          color: Colors.amber,
          size: 20,
        ),
        title: Text(
          title,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 15,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const AppLogo(
          type: AppLogoType.appBar,
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          stepTile('1', 'Canonical Name'),
          stepTile('2', 'Short Description'),
          stepTile('3', 'Definitions'),
          stepTile('4', 'Evidence'),
          stepTile('5', 'Aliases'),
          stepTile('6', 'Relationships'),
          stepTile('7', 'Review'),
          stepTile('8', 'Save Draft'),
          stepTile('9', 'Submit'),
        ],
      ),
    );
  }
}
