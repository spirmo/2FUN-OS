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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        automaticallyImplyLeading: false,
        backgroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
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
        title: Text(
          languageService.text("app_name"),
          style: const TextStyle(
            color: Colors.amber,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const SizedBox(height: 20),
            const CircleAvatar(
              radius: 45,
              backgroundColor: Colors.amber,
              child: Icon(
                Icons.person,
                size: 45,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              "Guest User",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 40),

            ListTile(
              leading: const Icon(Icons.school, color: Colors.amber),
              trailing: const Icon(Icons.chevron_right, color: Colors.grey),
              title: const Text(
                "Knowledge Injection",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {
                Navigator.pushNamed(context, '/knowledge-dashboard');
              },
            ),

            ListTile(
              leading: const Icon(Icons.menu_book, color: Colors.amber),
              trailing: const Icon(Icons.chevron_right, color: Colors.grey),
              title: const Text(
                "Knowledge",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.flag, color: Colors.amber),
              title: const Text(
                "Missions",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.groups, color: Colors.amber),
              title: const Text(
                "Colony",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.account_balance_wallet, color: Colors.amber),
              title: const Text(
                "Wallet",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.settings, color: Colors.amber),
              title: const Text(
                "Settings",
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {},
            ),

            const Spacer(),

            Text(
              languageService.text("app_name"),
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 14,
              ),
            ),

            const SizedBox(height: 8),

            Text(
              languageService.text("version"),
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 12,
              ),
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
