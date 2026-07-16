import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../core/routing/app_router.dart';
import '../../../../shared/widgets/app_logo.dart';

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
      elevation: 0,
      centerTitle: true,
      title: const SizedBox.shrink(),
    ),
    body: Stack(
      children: [
        const Positioned(
          top: 54,
          left: 0,
          right: 0,
          child: Center(
            child: AppLogo(
              type: AppLogoType.dashboard,
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              const SizedBox(height: 184),

              SizedBox(
                width: double.infinity,
                height: 46,
                child: ElevatedButton.icon(
                  icon: const Icon(
                    Icons.add_circle_outline,
                    size: 20,
                  ),
                  onPressed: () {
                    Navigator.pushNamed(
                      context,
                      AppRouter.wizard,
                    );
                  },
                  label: Text(
                    languageService.text("new_concept_package"),
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}
}
