import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';


class SourcesPage extends StatefulWidget {
  final int conceptId;
  final String conceptName;

  const SourcesPage({
    super.key,
    required this.conceptId,
    required this.conceptName,
  });

  @override
  State<SourcesPage> createState() => _SourcesPageState();
}

class _SourcesPageState extends State<SourcesPage> {
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
            children: const [
              SizedBox(height: 184),
            ],
          ),
        ],
      ),
    );
  }
}
