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
}
