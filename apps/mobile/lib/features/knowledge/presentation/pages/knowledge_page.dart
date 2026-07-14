import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../core/routing/app_router.dart';

class KnowledgePage extends StatefulWidget {
  const KnowledgePage({super.key});

  @override
  State<KnowledgePage> createState() => _KnowledgePageState();
}

class _KnowledgePageState extends State<KnowledgePage> {
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
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        centerTitle: true,
        title: Text(
          languageService.text("knowledge_production"),
          style: const TextStyle(
            color: Colors.amber,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: Center(
        child: ElevatedButton.icon(
          icon: const Icon(Icons.add_circle_outline),
          onPressed: () {
            Navigator.pushNamed(context, AppRouter.wizard);
          },
          label: Text(
            languageService.text("new_concept_package"),
          ),
        ),
      ),
    );
  }
}
