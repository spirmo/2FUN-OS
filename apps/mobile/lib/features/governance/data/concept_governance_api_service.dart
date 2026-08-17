import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../../core/config/app_config.dart';

class ConceptGovernanceApiService {

  Future<List<Map<String, dynamic>>> getPendingConcepts() async {

    final response = await http.get(
      Uri.parse(
        '${platformApiUrl}/concepts/pending',
      ),
    );

    final List data = jsonDecode(response.body);

    return data
        .map(
          (e) => Map<String, dynamic>.from(e),
        )
        .toList();
  }


  Future<Map<String, dynamic>> approveConcept(
    int queueId,
  ) async {

    final response = await http.post(
      Uri.parse(
        '${platformApiUrl}/concepts/$queueId/approve',
      ),
    );

    return Map<String, dynamic>.from(
      jsonDecode(response.body),
    );
  }

}
