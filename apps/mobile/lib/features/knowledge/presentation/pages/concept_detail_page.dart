import 'package:flutter/material.dart';

class ConceptDetailPage extends StatelessWidget {
  final int conceptId;

  const ConceptDetailPage({
    super.key,
    required this.conceptId,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Concept Detail"),
      ),
      body: Center(
        child: Text("Concept ID: $conceptId"),
      ),
    );
  }
}
