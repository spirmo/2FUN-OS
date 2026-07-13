import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
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
    return Card(
      color: const Color(0xFF1B1B1B),
      child: ListTile(
        leading: Icon(icon, color: Colors.amber),
        trailing: const Icon(Icons.chevron_right, color: Colors.grey),
        title: Text(
          title,
          style: const TextStyle(color: Colors.white),
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
        title: const Text(
          '2FUN',
          style: TextStyle(
            color: Colors.amber,
            fontWeight: FontWeight.bold,
          ),
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

          const Center(
            child: Text(
              'Guest User',
              style: TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          const SizedBox(height: 32),

          menuItem(
            icon: Icons.school,
            title: 'Knowledge Injection',
            onTap: () {
              Navigator.pushNamed(context, '/knowledge-dashboard');
            },
          ),

          menuItem(
            icon: Icons.menu_book,
            title: 'Knowledge',
          ),

          menuItem(
            icon: Icons.flag,
            title: 'Missions',
          ),

          menuItem(
            icon: Icons.groups,
            title: 'Colony',
          ),

          menuItem(
            icon: Icons.account_balance_wallet,
            title: 'Wallet',
          ),

          menuItem(
            icon: Icons.settings,
            title: 'Settings',
          ),

          const SizedBox(height: 32),

          const Center(
            child: Text(
              '2FUN Super App',
              style: TextStyle(color: Colors.grey),
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
