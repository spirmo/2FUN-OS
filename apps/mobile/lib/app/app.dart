import 'package:flutter/material.dart';

import '../core/routing/app_router.dart';
import '../core/theme/app_theme.dart';
import '../features/language/presentation/pages/splash_page.dart';

class TwoFunApp extends StatelessWidget {
  const TwoFunApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '2FUN',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const SplashPage(),
    );
  }
}
