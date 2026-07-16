import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';

class CreateDomainPage extends StatefulWidget {
  const CreateDomainPage({super.key});

  @override
  State<CreateDomainPage> createState() => _CreateDomainPageState();
}

class _CreateDomainPageState extends State<CreateDomainPage> {
  final LanguageService languageService = LanguageService();

  final TextEditingController codeController = TextEditingController();
  final TextEditingController faController = TextEditingController();
  final TextEditingController enController = TextEditingController();
  final TextEditingController arController = TextEditingController();
  final TextEditingController descriptionController =
      TextEditingController();

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

  Future<void> _saveDomain() async {
    final db = await DatabaseService.instance.database;

    await db.insert(
      'domains',
      {
        'code': codeController.text.trim(),
        'name_fa': faController.text.trim(),
        'name_en': enController.text.trim(),
        'name_ar': arController.text.trim(),
        'description': descriptionController.text.trim(),
        'status': 'PENDING',
        'created_at': DateTime.now().toIso8601String(),
      },
    );

    if (!mounted) return;

    Navigator.pop(context, true);
  }

  Widget field(
    String label,
    TextEditingController controller, {
    int maxLines = 1,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: SizedBox(
        height: maxLines == 1 ? 46 : null,
        child: TextField(
          controller: controller,
          maxLines: maxLines,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 14,
          ),
          decoration: InputDecoration(
            isDense: true,
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 12,
              vertical: 12,
            ),
            labelText: label,
            labelStyle: const TextStyle(
              color: Colors.amber,
              fontSize: 13,
            ),
            enabledBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: Colors.grey),
            ),
            focusedBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: Colors.amber),
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

            field("Domain Code", codeController),
            field("Persian Name", faController),
            field("English Name", enController),
            field("Arabic Name", arController),
            field(
              "Description",
              descriptionController,
              maxLines: 4,
            ),

            const SizedBox(height: 8),

            SizedBox(
              height: 46,
              child: ElevatedButton.icon(
                onPressed: _saveDomain,
                icon: const Icon(
                  Icons.save,
                  size: 20,
                ),
                label: const Text(
                  "Save",
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    ),
  );
}
}
