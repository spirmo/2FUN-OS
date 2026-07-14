import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../dashboard/presentation/pages/dashboard_page.dart';
import '../../../../core/language/language_service.dart';
import 'language_page.dart';
import 'welcome_page.dart';

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
      _start();
    });
  }

  Future<void> _start() async {
    final prefs = await SharedPreferences.getInstance();

    final language = await languageService.getLanguage();

    final welcomeSeen =
        prefs.getBool('welcome_seen') ?? false;

    if (!mounted) return;

    if (!welcomeSeen && language == 'fa') {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const LanguagePage(),
        ),
      );
      return;
    }

    await languageService.load(language);

    if (!mounted) return;

    if (!welcomeSeen) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const WelcomePage(),
        ),
      );
      return;
    }

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => const DashboardPage(),
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
