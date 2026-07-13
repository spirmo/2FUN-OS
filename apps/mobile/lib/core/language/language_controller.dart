import 'package:flutter/foundation.dart';

import 'language_model.dart';
import 'language_repository.dart';
import 'language_service.dart';

class LanguageController extends ChangeNotifier {
  final LanguageRepository repository = const LanguageRepository();
  final LanguageService service = LanguageService();

  List<LanguageModel> languages = [];
  String currentLanguage = 'fa';

  Future<void> initialize() async {
    languages = repository.getSupportedLanguages();

    currentLanguage = await service.getLanguage();

    await service.load(currentLanguage);

    notifyListeners();
  }

  Future<void> changeLanguage(String code) async {
    currentLanguage = code;

    await service.saveLanguage(code);

    notifyListeners();
  }

  String text(String key) {
    return service.text(key);
  }
}
