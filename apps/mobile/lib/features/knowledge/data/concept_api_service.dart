import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../../../core/config/app_config.dart';


class ConceptApiService {

  Future<Map<String, dynamic>> submitConcept({
    required Map<String, dynamic> payload,
  }) async {

    final response = await http.post(
      Uri.parse(
        '${platformApiUrl}/concepts/submit',
      ),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode(payload),
    );


    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> getPendingConcepts() async {
    final response = await http.get(
      Uri.parse(
        '${platformApiUrl}/concepts/pending',
      ),
    );

    return jsonDecode(response.body);
  }
