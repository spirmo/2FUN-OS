import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import 'domains_page.dart';

class KnowledgeDashboardPage extends StatefulWidget {
  const KnowledgeDashboardPage({super.key});

  @override
  State<KnowledgeDashboardPage> createState() =>
      _KnowledgeDashboardPageState();
}

class _KnowledgeDashboardPageState
    extends State<KnowledgeDashboardPage> {
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

  Widget item({
    required IconData icon,
    required String title,
    VoidCallback? onTap,
  }) {
    final enabled = onTap != null;

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 1),
      color: const Color(0xFF1B1B1B),
      child: SizedBox(
        height: 46,
        child: ListTile(
          dense: true,
          minLeadingWidth: 0,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 12,
            vertical: 0,
          ),
          leading: Icon(
            icon,
            size: 20,
            color: enabled ? Colors.amber : Colors.grey,
          ),
          trailing: Icon(
            Icons.chevron_right,
            size: 20,
            color: enabled ? Colors.amber : Colors.grey,
          ),
          title: Text(
            title,
            style: TextStyle(
              color: enabled ? Colors.white : Colors.grey,
              fontSize: 15,
            ),
          ),
          onTap: onTap,
        ),
      ),
    );
  }

  @override
Widget build(BuildContext context) {
  return Scaffold(
    backgroundColor: Colors.black,
    appBar: AppBar(
      backgroundColor: Colors.black,
      elevation: 0,
      centerTitle: true,
      title: const SizedBox.shrink(),
    ),
    body: Stack(
      children: [
        const Positioned(
          top: 54,
          left: 0,
          right: 0,
          child: Center(
            child: AppLogo(
              type: AppLogoType.dashboard,
            ),
          ),
        ),
        ListView(
          padding: const EdgeInsets.all(12),
          children: [
            const SizedBox(height: 184),

            item(
              icon: Icons.public,
              title: languageService.text("domains"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const DomainsPage(),
                  ),
                );
              },
            ),
            item(
              icon: Icons.folder_open,
              title: languageService.text("topics"),
            ),
            item(
              icon: Icons.lightbulb,
              title: languageService.text("concepts"),
            ),
            item(
              icon: Icons.sell,
              title: languageService.text("attributes"),
            ),
            item(
              icon: Icons.library_books,
              title: languageService.text("sources"),
            ),
            item(
              icon: Icons.translate,
              title: languageService.text("translations"),
            ),
            item(
              icon: Icons.quiz,
              title: languageService.text("questions"),
            ),
            item(
              icon: Icons.flag,
              title: languageService.text("missions"),
            ),
          ],
        ),
      ],
    ),
  );
}
}
