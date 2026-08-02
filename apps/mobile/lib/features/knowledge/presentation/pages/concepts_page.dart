import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import 'concept_detail_page.dart';
import 'create_concept_page.dart';

class ConceptsPage extends StatefulWidget {
  final int topicId;
  final String topicName;

  const ConceptsPage({
    super.key,
    required this.topicId,
    required this.topicName,
  });

  @override
  State<ConceptsPage> createState() =>
      _ConceptsPageState();
}

class _ConceptsPageState extends State<ConceptsPage> {
  final LanguageService languageService =
      LanguageService();

  List<Map<String, dynamic>> concepts = [];

  String currentLanguage = 'fa';

  @override
  void initState() {
    super.initState();

    _initialize();
  }

  Future<void> _initialize() async {
    await _loadLanguage();
    await _loadConcepts();
  }

  Future<void> _loadLanguage() async {
    final code =
        await languageService.getLanguage();

    currentLanguage = code;

    await languageService.load(code);

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _loadConcepts() async {
    final db =
        await DatabaseService.instance.database;

    final result = await db.query(
      'concepts',
      where: 'topic_id = ?',
      whereArgs: [
        widget.topicId,
      ],
      orderBy: 'id ASC',
    );

    if (mounted) {
      setState(() {
        concepts = result;
      });
    }
  }

  String _conceptName(
    Map<String, dynamic> concept,
  ) {
    switch (currentLanguage) {
      case 'en':
        return (concept['name_en'] ?? '')
            .toString();

      case 'ar':
        return (concept['name_ar'] ?? '')
            .toString();

      default:
        return (concept['name_fa'] ?? '')
            .toString();
    }
  }

  String _statusText(
    Map<String, dynamic> concept,
  ) {
    return (concept['status'] ?? 'PENDING')
        .toString();
  }

  Color _statusColor(
    String status,
  ) {
    switch (status) {
      case 'APPROVED':
        return Colors.green;

      case 'REJECTED':
        return Colors.red;

      case 'PENDING':
        return Colors.orange;

      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(
    BuildContext context,
  ) {
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
            padding:
                const EdgeInsets.all(12),

            children: [

              const SizedBox(
                height: 184,
              ),

              Text(
                widget.topicName,
                textAlign:
                    TextAlign.center,
                style:
                    const TextStyle(
                  color: Colors.amber,
                  fontSize: 20,
                  fontWeight:
                      FontWeight.bold,
                ),
              ),

              const SizedBox(
                height: 16,
              ),

              SizedBox(
                width:
                    double.infinity,

                height:
                    46,

                child:
                    ElevatedButton.icon(
                  icon:
                      const Icon(
                    Icons.add_circle_outline,
                  ),

                  label:
                      Text(
                    languageService.text(
                      "new_concept",
                    ),
                  ),

                  onPressed:
                      () async {

                    await Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            CreateConceptPage(
                          topicId:
                              widget.topicId,
                        ),
                      ),
                    );

                    await _loadConcepts();
                  },
                ),
              ),

              const SizedBox(
                height: 16,
              ),

              if (concepts.isEmpty)

                const Center(
                  child:
                      Text(
                    "NO CONCEPT",
                    style:
                        TextStyle(
                      color:
                          Colors.grey,
                    ),
                  ),
                )

              else

                ...concepts.map(
                  (concept) {

                    final status =
                        _statusText(
                          concept,
                        );

                    return Card(
                      color:
                          const Color(
                        0xFF1B1B1B,
                      ),

                      child:
                          ListTile(

                        onTap:
                            () async {

                          await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  ConceptDetailPage(
                                conceptId:
                                    concept['id'],
                              ),
                            ),
                          );

                          await _loadConcepts();
                        },

                        title:
                            Text(
                          _conceptName(
                            concept,
                          ),

                          style:
                              const TextStyle(
                            color:
                                Colors.white,
                            fontWeight:
                                FontWeight.bold,
                          ),
                        ),

                        subtitle:
                            Text(
                          "ID: ${concept['id']}\n"
                          "STATUS: $status",

                          style:
                              TextStyle(
                            color:
                                _statusColor(
                              status,
                            ),
                          ),
                        ),

                        trailing:
                            Icon(
                          Icons.arrow_forward_ios,
                          color:
                              _statusColor(
                            status,
                          ),
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
