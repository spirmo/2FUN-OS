import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/language/language_controller.dart';
import '../../../auth/presentation/pages/login_page.dart';

class LanguagePage extends StatefulWidget {
  const LanguagePage({super.key});

  @override
  State<LanguagePage> createState() => _LanguagePageState();
}

class _LanguagePageState extends State<LanguagePage> {
  final LanguageController controller = LanguageController();

  Future<void> saveLanguage(String language) async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.setString('app_language', language);
    await controller.changeLanguage(language);

    if (!mounted) return;

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => const LoginPage(),
      ),
    );
  }

  Widget languageButton({
    required String title,
    required VoidCallback onPressed,
  }) {
    return SizedBox(
      width: double.infinity,
      height: 56,
      child: ElevatedButton(
        onPressed: onPressed,
        child: Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const Spacer(),

              Image.asset(
                'assets/images/logo/logo.png',
                width: 180,
              ),

              const SizedBox(height: 24),

              const Text(
                'Choose Your Language',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 8),

              const Text(
                'زبان خود را انتخاب کنید',
                style: TextStyle(fontSize: 16),
              ),

              const Spacer(),

              languageButton(
                title: '🇮🇷 فارسی',
                onPressed: () => saveLanguage('fa'),
              ),

              const SizedBox(height: 16),

              languageButton(
                title: '🇺🇸 English',
                onPressed: () => saveLanguage('en'),
              ),

              const SizedBox(height: 16),

              languageButton(
                title: '🇸🇦 العربية',
                onPressed: () => saveLanguage('ar'),
              ),

              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}
