import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../auth/presentation/pages/login_page.dart';
import 'language_page.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  final LanguageService languageService = LanguageService();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkLanguage();
    });
  }

  Future<void> _checkLanguage() async {
    final language = await languageService.getLanguage();

    if (!mounted) return;

    if (language.isEmpty) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => const LanguagePage(),
        ),
      );
      return;
    }

    await languageService.load(language);

    if (!mounted) return;

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => const LoginPage(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
