import 'concepts_page.dart';
import '../../../../core/database/database_service.dart';
import 'create_topic_page.dart';
import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';


class TopicsPage extends StatefulWidget {
  final int domainId;
  final String domainName;

  const TopicsPage({
    super.key,
    required this.domainId,
    required this.domainName,
  });

  @override
  State<TopicsPage> createState() => _TopicsPageState();
}

class _TopicsPageState extends State<TopicsPage> {
  final LanguageService languageService = LanguageService();
    List<Map<String, dynamic>> topics = [];
  @override
  void initState() {
    super.initState();
    _loadLanguage();
    _loadTopics();
}
  Future<void> _loadTopics() async {
  final db = await DatabaseService.instance.database;

  final result = await db.query(
    'topics',
    where: 'domain_id=?',
    whereArgs: [widget.domainId],
    orderBy: 'id DESC',
  );

  if (mounted) {
    setState(() {
      topics = result;
    });
  }
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
              SizedBox(height: 184),
              SizedBox(
              width: double.infinity,
              height: 46,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.add_circle_outline),
                label: Text(
                  languageService.text("new_topic"),
                ),                 
                onPressed: () async {
                      await Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => CreateTopicPage(
                            domainId: widget.domainId,
                          ),
                        ),
                      );

                      _loadTopics();
                    },
                  ),
                ),

const SizedBox(height: 12),
              ListTile(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => ConceptsPage(
                        topicId: t["id"],
                        topicName: t["name_fa"],
                      ),
                    ),
                  );
                },
                title: Text(
                  t["name_fa"].toString(),
                  style: const TextStyle(color: Colors.white),
                ),
                subtitle: Text(
                  t["name_en"].toString(),
                  style: const TextStyle(color: Colors.grey),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
