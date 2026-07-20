import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';

class CreateConceptPage extends StatefulWidget {
  final int topicId;

  const CreateConceptPage({
    super.key,
    required this.topicId,
  });

  @override
  State<CreateConceptPage> createState() =>
      _CreateConceptPageState();
}

class _CreateConceptPageState extends State<CreateConceptPage> {
  final LanguageService languageService = LanguageService();

  final Map<String, TextEditingController> controllers = {};

  final List<String> fields = [

    // Mandatory 11
    "title_fa",
    "domain",
    "category",
    "canonical_meaning",
    "definition",
    "short_description",
    "source",
    "source_url",
    "source_author",
    "source_year",
    "evidence",

    // Optional 25
    "title_en",
    "title_ar",
    "other_languages",
    "translations",
    "translation_language",
    "translated_text",
    "related_concepts",
    "features",
    "feature_value",
    "questions",
    "answers",
    "missions",
    "mission_title",
    "mission_description",
    "tags",
    "difficulty",
    "notes",
    "images",
    "videos",
    "attachments",
    "examples",
    "counter_examples",
    "additional_sources",
    "validation_notes",
    "future_development",
  ];

  @override
  void initState() {
    super.initState();

    _createControllers();
    _loadLanguage();
  }

  void _createControllers() {
    for (final key in fields) {
      controllers[key] = TextEditingController();
    }
  }

  Future<void> _loadLanguage() async {
    final code = await languageService.getLanguage();

    await languageService.load(code);

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _saveConcept() async {
    final Map<String, String> items = {};

    for (final key in fields) {
      items[key] = controllers[key]!.text.trim();
    }

    final requiredKeys = fields.take(11);

for (final key in requiredKeys) {
  if (items[key]!.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          "Required field missing: $key",
        ),
      ),
    );

    return;
  }
}

final conceptId =
    await DatabaseService.instance.createFullConcept(
  topicId: widget.topicId,
  items: items,
);

    if (!mounted) return;

    Navigator.pop(
      context,
      true,
    );
  }

  Widget field(
        String key, {
           int maxLines = 1,
         }) {
           return Padding(
             padding: const EdgeInsets.only(
               bottom: 10,
             ),
             child: TextField(
               controller: controllers[key],
               maxLines: maxLines,
               style: const TextStyle(
                 color: Colors.white,
               ),
               decoration: InputDecoration(
                 labelText: languageService.text(key),

                 hintText: languageService.text("${key}_hint"),

                 hintStyle: const TextStyle(
                   color: Colors.white38,
                   fontSize: 13,
                 ),

                 labelStyle: const TextStyle(
                   color: Colors.amber,
                 ),
  
          enabledBorder: const OutlineInputBorder(
            borderSide: BorderSide(
              color: Colors.grey,
            ),
          ),

          focusedBorder: const OutlineInputBorder(
            borderSide: BorderSide(
              color: Colors.amber,
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

        title: Text(
          languageService.text(
            "new_concept",
          ),
        ),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: ListView(
          children: [

            const Text(
              "Mandatory Items",
              style: TextStyle(
                color: Colors.amber,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            ...fields
                .take(11)
                .map(
                  (e) => field(
                    e,
                    maxLines:
                        e == "definition" ||
                        e == "evidence" ||
                        e == "canonical_meaning"
                            ? 4
                            : 1,
                  ),
                ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              "Optional Items",
              style: TextStyle(
                color: Colors.amber,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            ...fields
                .skip(11)
                .map(
                  (e) => field(
                    e,
                    maxLines: 3,
                  ),
                ),

            const SizedBox(
              height: 20,
            ),

            SizedBox(
              width: double.infinity,

              child: ElevatedButton(
                onPressed: _saveConcept,

                child: Text(
                  languageService.text(
                    "save",
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    for (final controller in controllers.values) {
      controller.dispose();
    }

    super.dispose();
  }
}
