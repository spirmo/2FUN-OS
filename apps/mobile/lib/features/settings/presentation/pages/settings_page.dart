import 'package:flutter/material.dart';

import '../../../../core/database/database_export_service.dart';
import '../../../../core/language/language_service.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {

  final LanguageService languageService = LanguageService();

  String? exportPath;

  Future<void> _exportDatabase() async {

    final path =
        await DatabaseExportService.exportDatabase();

    setState(() {
      exportPath = path;
    });

  }


  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text(
          languageService.text("settings"),
          style: const TextStyle(
            color: Colors.white,
          ),
        ),
      ),


      body: Padding(

        padding: const EdgeInsets.all(16),

        child: Column(

          children: [

            ListTile(
              leading: const Icon(
                Icons.language,
                color: Colors.amber,
              ),

              title: Text(
                languageService.text("language"),
                style: const TextStyle(
                  color: Colors.white,
                ),
              ),

            ),


            ListTile(

              leading: const Icon(
                Icons.storage,
                color: Colors.amber,
              ),

              title: const Text(
                "Export Database",
                style: TextStyle(
                  color: Colors.white,
                ),
              ),

              onTap: _exportDatabase,

            ),


            if(exportPath != null)

              Text(
                exportPath!,
                style: const TextStyle(
                  color: Colors.grey,
                  fontSize: 12,
                ),
              ),


          ],

        ),

      ),

    );

  }

}
