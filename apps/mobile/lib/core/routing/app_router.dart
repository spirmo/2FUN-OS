import 'package:flutter/material.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/knowledge/presentation/pages/knowledge_dashboard_page.dart';
import '../../features/knowledge/presentation/pages/knowledge_page.dart';
import '../../features/language/presentation/pages/language_page.dart';
import '../../features/wizard/presentation/pages/wizard_page.dart';

class AppRouter {
  static const login = '/';
  static const dashboard = '/dashboard';
  static const knowledge = '/knowledge';
  static const wizard = '/wizard';
  static const language = '/language';
  static const knowledgeDashboard = '/knowledge-dashboard';

  static Route<dynamic> generate(RouteSettings settings) {
    switch (settings.name) {
      case login:
        return MaterialPageRoute(
          builder: (_) => const LoginPage(),
        );

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

      case language:
        return MaterialPageRoute(
          builder: (_) => const LanguagePage(),
        );

      case knowledgeDashboard:
        return MaterialPageRoute(
          builder: (_) => const KnowledgeDashboardPage(),
        );

      default:
        return MaterialPageRoute(
          builder: (_) => const LanguagePage(),
        );
    }
  }
}
