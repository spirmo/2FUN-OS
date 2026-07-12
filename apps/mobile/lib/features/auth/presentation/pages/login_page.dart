import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

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

  Future<void> launchTelegramLogin() async {
    final uri = Uri.parse("https://t.me/twofun_bot");

    if (!await launchUrl(
      uri,
      mode: LaunchMode.externalApplication,
    )) {
      throw Exception("Could not launch Telegram");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Center(
            child: SingleChildScrollView(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const AppLogo(),

                  const SizedBox(height: 40),

                  PrimaryButton(
                    text: languageService.text("continue_telegram"),
                    icon: Icons.telegram,
                    onPressed: () async {
                      await launchTelegramLogin();
                    },
                  ),

                  const SizedBox(height: 16),

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

                  const SizedBox(height: 40),

                  Text(
                    languageService.text("powered_by"),
                    textAlign: TextAlign.center,
                  ),

                  const SizedBox(height: 12),

                  Text(
                    languageService.text("founder"),
                    textAlign: TextAlign.center,
                  ),

                  const SizedBox(height: 20),

                  Text(
                    languageService.text("copyright"),
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 11),
                  ),

                  const SizedBox(height: 16),

                  Text(
                    languageService.text("version"),
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
