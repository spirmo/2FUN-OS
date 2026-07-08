import 'package:flutter/material.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/knowledge/presentation/pages/knowledge_page.dart';
import '../../features/wizard/presentation/pages/wizard_page.dart';

class AppRouter {
  static const login = '/';
  static const dashboard = '/dashboard';
  static const knowledge = '/knowledge';
  static const wizard = '/wizard';

  static Route<dynamic> generate(RouteSettings settings) {
    switch (settings.name) {
      case dashboard:
        return MaterialPageRoute(
          builder: (_) => const DashboardPage(),
        );

      case knowledge:
        return MaterialPageRoute(
          builder: (_) => const KnowledgePage(),
        );

      case wizard:
        return MaterialPageRoute(
          builder: (_) => const WizardPage(),
        );

      case login:
      default:
        return MaterialPageRoute(
          builder: (_) => const LoginPage(),
        );
    }
  }
}
