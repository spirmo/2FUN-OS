import 'package:flutter/material.dart';

import '../core/language/language_controller.dart';
import '../core/routing/app_router.dart';
import '../core/theme/app_theme.dart';
import '../features/language/presentation/pages/splash_page.dart';

class TwoFunApp extends StatefulWidget {
  const TwoFunApp({super.key});

  @override
  State<TwoFunApp> createState() => _TwoFunAppState();
}

class _TwoFunAppState extends State<TwoFunApp> {
  final LanguageController languageController = LanguageController();

  @override
  void initState() {
    super.initState();
    // Initialization intentionally disabled for startup stability test.
  }

  @override
  void dispose() {
    languageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: languageController,
      builder: (context, _) {
        return MaterialApp(
          title: "2FUN",
          debugShowCheckedModeBanner: false,
          theme: AppTheme.darkTheme,
          locale: const Locale("fa"),
          onGenerateRoute: AppRouter.generate,
          home: const SplashPage(),
        );
      },
    );
  }
}
