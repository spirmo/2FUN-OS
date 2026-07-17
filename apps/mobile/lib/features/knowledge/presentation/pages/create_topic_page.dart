import 'package:flutter/material.dart';

class CreateTopicPage extends StatefulWidget {
  final int domainId;

  const CreateTopicPage({
    super.key,
    required this.domainId,
  });

  @override
  State<CreateTopicPage> createState() => _CreateTopicPageState();
}

class _CreateTopicPageState extends State<CreateTopicPage> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.black,
    );
  }
}
