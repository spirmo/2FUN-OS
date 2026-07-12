import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageService {
  static const _key = 'app_language';

  Map<String, dynamic> _translations = {};

  Future<void> saveLanguage(String code) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, code);
    await load(code);
  }

  Future<String> getLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_key) ?? 'fa';
  }

  Future<void> clearLanguage() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
    _translations = {};
  }

  Future<void> load(String languageCode) async {
    try {
      final jsonString = await rootBundle.loadString(
        'assets/translations/$languageCode.json',
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
