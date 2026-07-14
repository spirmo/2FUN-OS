import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';

class CreateDomainPage extends StatefulWidget {
  CreateDomainPage({super.key});

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

  Widget field(
    String label,
    TextEditingController controller, {
    int maxLines = 1,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextField(
        controller: controller,
        maxLines: maxLines,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: const TextStyle(color: Colors.amber),
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text("Create Domain"),
        centerTitle: true,
        backgroundColor: Colors.black,
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          field("Domain Code", codeController),
          field("Persian Name", faController),
          field("English Name", enController),
          field("Arabic Name", arController),
          field(
            "Description",
            descriptionController,
            maxLines: 4,
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text("Domain saved successfully"),
                ),
              );
            },
            icon: const Icon(Icons.save),
            label: const Text("Save"),
          ),
        ],
      ),
    );
  }
}
