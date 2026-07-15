import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import '../../../language/presentation/pages/language_page.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
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

  Widget menuItem({
    required IconData icon,
    required String title,
    VoidCallback? onTap,
  }) {
    final enabled = onTap != null;

    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: Icon(
          icon,
          color: enabled ? Colors.amber : Colors.grey,
        ),
        trailing: Icon(
          Icons.chevron_right,
          color: enabled ? Colors.amber : Colors.grey,
        ),
        title: Text(
          title,
          style: TextStyle(
            color: enabled ? Colors.white : Colors.grey,
          ),
        ),
        onTap: onTap,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        automaticallyImplyLeading: false,
        backgroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const AppLogo(
          type: AppLogoType.appBar,
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.language),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const LanguagePage(),
                ),
              );
            },
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const SizedBox(height: 12),

          const CircleAvatar(
            radius: 45,
            backgroundColor: Colors.amber,
            child: Icon(
              Icons.person,
              size: 45,
              color: Colors.black,
            ),
          ),

          const SizedBox(height: 16),

          Center(
            child: Text(
              languageService.text("continue_guest"),
              style: const TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          const SizedBox(height: 32),

          menuItem(
            icon: Icons.psychology,
            title: languageService.text("knowledge_injection"),
            onTap: () {
              Navigator.pushNamed(context, '/knowledge-dashboard');
            },
          ),

          menuItem(
            icon: Icons.menu_book,
            title: languageService.text("knowledge"),
          ),

          menuItem(
            icon: Icons.flag,
            title: languageService.text("missions"),
          ),

          menuItem(
            icon: Icons.groups,
            title: languageService.text("colony"),
          ),

          menuItem(
            icon: Icons.account_balance_wallet,
            title: languageService.text("wallet"),
          ),

          menuItem(
            icon: Icons.settings,
            title: languageService.text("settings"),
          ),

          const SizedBox(height: 32),

          Center(
            child: Text(
              languageService.text("app_name"),
              style: const TextStyle(color: Colors.grey),
            ),
          ),

          const SizedBox(height: 8),

          Center(
            child: Text(
              languageService.text("version"),
              style: const TextStyle(color: Colors.grey),
            ),
          ),
        ],
      ),
    );
  }
}
