import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import '../../../dashboard/presentation/pages/dashboard_page.dart';

class WelcomePage extends StatefulWidget {
  const WelcomePage({super.key});

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  final LanguageService languageService = LanguageService();

  final ScrollController _scrollController = ScrollController();

  bool rtl = true;
  bool canStart = false;

  @override
  void initState() {
    super.initState();

    _loadLanguage();

    _scrollController.addListener(() {
      if (_scrollController.position.pixels >=
              _scrollController.position.maxScrollExtent - 20 &&
          !canStart) {
        setState(() {
          canStart = true;
        });
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _loadLanguage() async {
    final code = await languageService.getLanguage();

    await languageService.load(code);

    rtl = code == "fa" || code == "ar";

    if (mounted) {
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection:
          rtl ? TextDirection.rtl : TextDirection.ltr,
      child: Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(
          backgroundColor: Colors.black,
          centerTitle: true,
          title: Text(
            languageService.text("welcome_title"),
            style: const TextStyle(
              color: Colors.amber,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        body: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              const AppLogo(width: 162),

              const SizedBox(height: 24),

              Text(
                languageService.text("welcome_quote"),
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.amber,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  height: 1.8,
                ),
              ),

              const SizedBox(height: 24),

              Expanded(
                child: SingleChildScrollView(
                  controller: _scrollController,
                  child: Text(
                    languageService.text("welcome_text"),
                    textAlign:
                        rtl ? TextAlign.right : TextAlign.left,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 17,
                      height: 1.8,
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 20),

              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: canStart
                      ? () async {
                          final prefs =
                              await SharedPreferences.getInstance();

                          await prefs.setBool(
                            'welcome_seen',
                            true,
                          );

                          if (!mounted) return;

                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  const DashboardPage(),
                            ),
                          );
                        }
                      : null,
                  child: Text(
                    languageService.text("start_journey"),
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 10),
            ],
          ),
        ),
      ),
    );
  }
}
