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
  
  final _faController = TextEditingController();
  final _enController = TextEditingController();
  @override
Widget build(BuildContext context) {
  return Scaffold(
    backgroundColor: Colors.black,
    appBar: AppBar(
      backgroundColor: Colors.black,
      title: const Text("موضوع جدید"),
    ),
    body: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          TextField(
            controller: _faController,
            decoration: const InputDecoration(
              labelText: "عنوان فارسی",
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _enController,
            decoration: const InputDecoration(
              labelText: "English Title",
            ),
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {},
              child: const Text("ثبت موضوع"),
            ),
          ),
        ],
      ),
    ),
  );
}
}
