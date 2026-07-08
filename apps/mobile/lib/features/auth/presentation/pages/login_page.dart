import 'package:flutter/material.dart';
import '../../../../../core/routing/app_router.dart';
import '../../../../../core/constants/app_strings.dart';
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
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const AppLogo(),

                const SizedBox(height: 40),

                PrimaryButton(
                  text: AppStrings.continueTelegram,
                  icon: Icons.telegram,
                  onPressed: () {
                  Navigator.pushNamed(context, AppRouter.dashboard);
                  },

                const SizedBox(height: 16),

                SecondaryButton(
                  text: AppStrings.continueGuest,
                  icon: Icons.person_outline,
                  onPressed: () {
                  Navigator.pushNamed(context, AppRouter.dashboard);
                  },

                const SizedBox(height: 40),

                const Text(AppStrings.poweredBy),

                const SizedBox(height: 8),

                const Text(AppStrings.version),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
