import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/country.dart';

class CountryService {
  Future<List<Country>> loadCountries() async {
    final jsonString =
        await rootBundle.loadString('assets/data/countries.json');

    final List<dynamic> data = json.decode(jsonString);

    return data
        .map((e) => Country.fromJson(e))
        .toList();
  }
}
