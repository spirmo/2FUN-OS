import 'language_model.dart';

class LanguageRepository {
  const LanguageRepository();

  List<LanguageModel> getSupportedLanguages() {
    return const [
      LanguageModel(
        code: 'fa',
        name: 'Persian',
        nativeName: 'فارسی',
        rtl: true,
      ),
      LanguageModel(
        code: 'en',
        name: 'English',
        nativeName: 'English',
        rtl: false,
      ),
      LanguageModel(
        code: 'ar',
        name: 'Arabic',
        nativeName: 'العربية',
        rtl: true,
      ),
    ];
  }
}
