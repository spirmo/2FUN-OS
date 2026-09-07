import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageService {
  static const _key = 'app_language';

  Map<String, dynamic> _translations = {};

  String _effectiveLanguage(String code) {
    switch (code) {
      case 'fa':
        return 'fa';
      case 'ar':
        return 'ar';
      case 'en':
        return 'en';
      default:
        return 'en';
    }
  }

  Future<void> saveLanguage(String code) async {
    final language = _effectiveLanguage(code);

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, language);

    await load(language);
  }

  Future<String> getLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    final stored = prefs.getString(_key) ?? 'fa';

    return _effectiveLanguage(stored);
  }

  Future<void> clearLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
    _translations = {};
  }

  Future<void> load(String languageCode) async {
    final language = _effectiveLanguage(languageCode);

    try {
      final jsonString = await rootBundle.loadString(
        'assets/translations/$language.json',
      );

      _translations = json.decode(jsonString);
    } catch (_) {
      _translations = {};
    }
  }

  String text(String key) {
    return _translations[key]?.toString() ?? key;
  }
}
