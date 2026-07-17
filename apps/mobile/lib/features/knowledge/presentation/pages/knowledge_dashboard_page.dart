import 'concepts_page.dart';
import 'attributes_page.dart';
import 'sources_page.dart';
import 'translations_page.dart';
import 'questions_page.dart';
import 'missions_page.dart';
import 'topics_page.dart';
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
      height: 52,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Row(
            children: [
              SizedBox(
                width: 26,
                child: Center(
                  child: Icon(
                    icon,
                    size: 20,
                    color: enabled ? Colors.amber : Colors.grey,
                  ),
                ),
              ),

              const SizedBox(width: 10),

              Expanded(
                child: Text(
                  title,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    color: enabled ? Colors.white : Colors.grey,
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),

              SizedBox(
                width: 26,
                child: Center(
                  child: Icon(
                    Icons.chevron_right,
                    size: 20,
                    color: enabled ? Colors.amber : Colors.grey,
                  ),
                ),
              ),
            ],
          ),
        ),
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
          top: 18,
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
             onTap: () {
               Navigator.push(
                 context,
                MaterialPageRoute(
                   builder: (_) => const TopicsPage(
                      domainId: 0,
                      domainName: '',
                   ),
                 ),
               );
             },
           ),
            item(
              icon: Icons.lightbulb,
              title: languageService.text("concepts"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const ConceptsPage(
                      topicId: 0,
                      topicName: '',
                    ),
                  ),
                );
              },
            ),         
            item(
              icon: Icons.sell,
              title: languageService.text("attributes"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const AttributesPage(
                      conceptId: 0,
                      conceptName: '',
                    ),
                  ),
                );
              },
            ),      
            item(
              icon: Icons.library_books,
              title: languageService.text("sources"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const SourcesPage(
                      conceptId: 0,
                      conceptName: '',
                    ),
                  ),
                );
              },
            ),
            
            item(
              icon: Icons.translate,
              title: languageService.text("translations"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const TranslationsPage(
                      conceptId: 0,
                      conceptName: '',
                    ),
                  ),
                );
              },
            ),   
            item(
              icon: Icons.quiz,
              title: languageService.text("questions"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const QuestionsPage(
                      conceptId: 0,
                      conceptName: '',
                    ),
                  ),
                );
              },
            ),
            
            item(
              icon: Icons.flag,
              title: languageService.text("missions"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const MissionsPage(
                      conceptId: 0,
                      conceptName: '',
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ],
    ),
  );
}
}
