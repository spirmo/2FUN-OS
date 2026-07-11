import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../../../core/constants/app_strings.dart';
import '../../../../../core/routing/app_router.dart';
import '../../../../../shared/widgets/app_logo.dart';
import '../../../../../shared/widgets/buttons/primary_button.dart';
import '../../../../../shared/widgets/buttons/secondary_button.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

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
                    text:
                        '${AppStrings.continueTelegramFa}\n${AppStrings.continueTelegramEn}',
                    icon: Icons.telegram,
                    onPressed: () async {
                      await launchTelegramLogin();
                    },
                  ),

                  const SizedBox(height: 16),

                  SecondaryButton(
                    text:
                        '${AppStrings.continueGuestFa}\n${AppStrings.continueGuestEn}',
                    icon: Icons.person_outline,
                    onPressed: () {
                      Navigator.pushReplacementNamed(
                        context,
                        AppRouter.dashboard,
                      );
                    },
                  ),

                  const SizedBox(height: 40),

                  const Text(
                    '${AppStrings.poweredByFa}\n${AppStrings.poweredByEn}',
                    textAlign: TextAlign.center,
                  ),

                  const SizedBox(height: 12),

                  const Text(
                    '${AppStrings.founderFa}\n${AppStrings.founderEn}',
                    textAlign: TextAlign.center,
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    '${AppStrings.copyrightFa}\n\n${AppStrings.copyrightEn}',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 11),
                  ),

                  const SizedBox(height: 16),

                  const Text(AppStrings.version),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
