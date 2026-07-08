import 'package:flutter/material.dart';

import '../../../../core/routing/app_router.dart';

class KnowledgePage extends StatelessWidget {
  const KnowledgePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Knowledge Production'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pushNamed(context, AppRouter.wizard);
          },
          child: const Text('New Concept Package'),
        ),
      ),
    );
  }
}
