import 'package:flutter/material.dart';

import '../../../../../core/constants/app_strings.dart';
import '../../../../../core/routing/app_router.dart';
import '../../../../../shared/widgets/app_logo.dart';
import '../../../../../shared/widgets/buttons/primary_button.dart';
import '../../../../../shared/widgets/buttons/secondary_button.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

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
                    onPressed: () {
                      Navigator.pushNamed(context, AppRouter.dashboard);
                    },
                  ),

                  const SizedBox(height: 16),

                  SecondaryButton(
                    text:
                        '${AppStrings.continueGuestFa}\n${AppStrings.continueGuestEn}',
                    icon: Icons.person_outline,
                    onPressed: () {
                      Navigator.pushNamed(context, AppRouter.dashboard);
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
