import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/language/language_controller.dart';
import '../../../../core/services/country_service.dart';
import '../../../../core/models/country.dart';
import '../../language/presentation/pages/welcome_page.dart';

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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        centerTitle: true,
        title: const Text(
          "Select Country",
          style: TextStyle(color: Colors.amber),
        ),
      ),
      body: countries.isEmpty
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : ListView.builder(
              itemCount: countries.length,
              itemBuilder: (context, index) {
                final country = countries[index];

                return ListTile(
                  leading: Text(
                    country.flag,
                    style: const TextStyle(fontSize: 26),
                  ),
                  title: Text(
                    country.nameEn,
                    style: const TextStyle(color: Colors.white),
                  ),
                  subtitle: Text(
                    country.nameFa,
                    style: const TextStyle(color: Colors.grey),
                  ),
                  onTap: () => selectCountry(country),
                );
              },
            ),
    );
  }
}
