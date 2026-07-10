import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';

class LanguagePage extends StatelessWidget {
  const LanguagePage({super.key});
  Future<void> saveLanguage(BuildContext context, String language) async {
  final prefs = await SharedPreferences.getInstance();

  await prefs.setString('app_language', language);

  if (context.mounted) {
    Navigator.pushReplacementNamed(context, '/');
  }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Spacer(),

                Image.asset(
                  'assets/images/logo/logo.png',
                  width: 200,
                ),

                const Spacer(),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(     
                    onPressed: () {
                      saveLanguage(context, 'fa');
                    },                                        
                      Navigator.pushReplacementNamed(context, '/');
                    },                                      
                    child: const Text("🇮🇷 فارسی"),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(                    
                    onPressed: () {
                      saveLanguage(context, 'en');
                    },                                    
                      Navigator.pushReplacementNamed(context, '/');
                    },                    
                    child: const Text("🇺🇸 English"),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(     
                    onPressed: () {
                      saveLanguage(context, 'ar');
                    },                                  
                      Navigator.pushReplacementNamed(context, '/');
                    },   
                    child: const Text("🇸🇦 العربية"),
                  ),
                ),

                const Spacer(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
