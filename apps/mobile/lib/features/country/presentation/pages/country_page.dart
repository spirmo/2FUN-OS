import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/language/language_controller.dart';
import '../../../../core/models/country.dart';
import '../../../../core/services/country_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import '../../../language/presentation/pages/welcome_page.dart';

class CountryPage extends StatefulWidget {
  const CountryPage({super.key});

  @override
  State<CountryPage> createState() => _CountryPageState();
}

class _CountryPageState extends State<CountryPage> {
  final CountryService service = CountryService();
  final LanguageController controller = LanguageController();

  List<Country> countries = [];

  @override
  void initState() {
    super.initState();
    loadCountries();
  }

  Future<void> loadCountries() async {
    countries = await service.loadCountries();

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> selectCountry(Country country) async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.setInt("country_id", country.id);
    await prefs.setString("app_language", country.language);

    await controller.changeLanguage(country.language);

    if (!mounted) return;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => const WelcomePage(),
      ),
    );
  }

  Widget countryCard(Country country) {
    return InkWell(
      borderRadius: BorderRadius.circular(14),
      onTap: () => selectCountry(country),
      child: Card(
        color: const Color(0xFF1B1B1B),
        child: Padding(
          padding: const EdgeInsets.symmetric(
            vertical: 18,
            horizontal: 8,
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                country.flag,
                style: const TextStyle(fontSize: 34),
              ),
              const SizedBox(height: 10),
              Text(
                country.nameEn,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                country.nameFa,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.grey,
                  fontSize: 12,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: countries.isEmpty
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    const SizedBox(height: 12),

                    const AppLogo(
                      width: 180,
                    ),

                    const SizedBox(height: 20),

                    const Text(
                      "2FUN Super App",
                      style: TextStyle(
                        color: Colors.amber,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 10),

                    const Text(
                      "کشور خود را انتخاب کنید",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),

                    const SizedBox(height: 24),

                    Expanded(
                      child: GridView.builder(
                        itemCount: countries.length,
                        gridDelegate:
                            const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 3,
                          crossAxisSpacing: 12,
                          mainAxisSpacing: 12,
                          childAspectRatio: 0.9,
                        ),
                        itemBuilder: (context, index) {
                          return countryCard(countries[index]);
                        },
                      ),
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
