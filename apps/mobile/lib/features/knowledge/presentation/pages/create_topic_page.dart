import '../../../../core/language/language_service.dart';
import '../../../../core/database/database_service.dart';
import 'package:flutter/material.dart';

class CreateTopicPage extends StatefulWidget {
  final int domainId;

  const CreateTopicPage({
    super.key,
    required this.domainId,
  });

  @override
  State<CreateTopicPage> createState() => _CreateTopicPageState();
}

class _CreateTopicPageState extends State<CreateTopicPage> {

  final _faController = TextEditingController();
  final _enController = TextEditingController();

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
        backgroundColor: Colors.black,
        title: Text(
          languageService.text("new_topic"),
        ),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [

            TextField(
              controller: _faController,
              decoration: InputDecoration(
                labelText: languageService.text("name_fa"),
              ),
            ),

            const SizedBox(height: 12),

            TextField(
              controller: _enController,
              decoration: InputDecoration(
                labelText: languageService.text("name_en"),
              ),
            ),

            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,

              child: ElevatedButton(

                onPressed: () async {

                  await DatabaseService.instance.insertTopic(
                    domainId: widget.domainId,
                    fa: _faController.text,
                    en: _enController.text,
                  );

                  if (mounted) {
                    Navigator.pop(context);
                  }
                },

                child: Text(
                  languageService.text("save"),
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
    _faController.dispose();
    _enController.dispose();
    super.dispose();
  }
}
