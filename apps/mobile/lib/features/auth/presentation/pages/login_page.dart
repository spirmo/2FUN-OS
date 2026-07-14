import 'package:flutter/material.dart';

import '../../../../../core/language/language_service.dart';
import '../../../../../core/routing/app_router.dart';
import '../../../../../shared/widgets/app_logo.dart';
import '../../../../../shared/widgets/buttons/primary_button.dart';
import '../../../../../shared/widgets/buttons/secondary_button.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
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
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Center(
            child: SingleChildScrollView(
              child: Column(
                children: [
                  const AppLogo(width: 170),

                  const SizedBox(height: 20),

                  Text(
                    languageService.text("app_name"),
                    style: const TextStyle(
                      color: Colors.amber,
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 40),

                  PrimaryButton(
                    text: languageService.text("continue_telegram"),
                    icon: Icons.telegram,
                    onPressed: () {
                      // Telegram Login (در نسخه بعدی فعال می‌شود)
                    },
                  ),

                  const SizedBox(height: 18),

                  SecondaryButton(
                    text: languageService.text("continue_guest"),
                    icon: Icons.person_outline,
                    onPressed: () {
                      Navigator.pushReplacementNamed(
                        context,
                        AppRouter.dashboard,
                      );
                    },
                  ),

                  const SizedBox(height: 45),

                  Text(
                    languageService.text("powered_by"),
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.grey),
                  ),

                  const SizedBox(height: 10),

                  Text(
                    languageService.text("founder"),
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white70),
                  ),

                  const SizedBox(height: 18),

                  Text(
                    languageService.text("copyright"),
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 11,
                      color: Colors.grey,
                    ),
                  ),

                  const SizedBox(height: 14),

                  Text(
                    languageService.text("version"),
                    style: const TextStyle(color: Colors.amber),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
