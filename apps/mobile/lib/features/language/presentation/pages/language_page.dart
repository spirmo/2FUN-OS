import 'package:flutter/material.dart';

import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/language/language_controller.dart';
import '../../../auth/presentation/pages/login_page.dart';

class LanguagePage extends StatelessWidget {
  LanguagePage({super.key});

  final LanguageController controller = LanguageController();

  Future<void> saveLanguage(
    BuildContext context,
    String language,
  ) async {
    // برای سازگاری با Splash
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('app_language', language);

    // بروزرسانی کنترلر زبان
    await controller.changeLanguage(language);

    if (!context.mounted) return;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => const LoginPage(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Spacer(),

                Image.asset(
                  'assets/images/logo/logo.png',
                  width: 200,
                ),

                const Spacer(),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => saveLanguage(context, 'fa'),
                    child: const Text("🇮🇷 فارسی"),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => saveLanguage(context, 'en'),
                    child: const Text("🇺🇸 English"),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => saveLanguage(context, 'ar'),
                    child: const Text("🇸🇦 العربية"),
                  ),
                ),

                const Spacer(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
