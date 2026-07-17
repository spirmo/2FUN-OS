import 'package:flutter/material.dart';

class CreateConceptPage extends StatefulWidget {
  final int topicId;

  const CreateConceptPage({
    super.key,
    required this.topicId,
  });

  @override
  State<CreateConceptPage> createState() => _CreateConceptPageState();
}

class _CreateConceptPageState extends State<CreateConceptPage> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.black,
    );
  }
}
