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

  Future<Map<String, dynamic>> getConcepts() async {
    final response = await http.get(
      Uri.parse(
        '${platformApiUrl}/concepts',
      ),
    );

    return jsonDecode(response.body);
  }
  Future<Map<String, dynamic>> getConcept({
    required String conceptCode,
  }) async {
    final response = await http.get(
      Uri.parse(
        '${platformApiUrl}/concepts/$conceptCode?version=1.0',
      ),
    );

    return jsonDecode(response.body);
  }

}
