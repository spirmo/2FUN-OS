import 'package:flutter/material.dart';

import '../../../../core/routing/app_router.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('2FUN Dashboard'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pushNamed(context, AppRouter.knowledge);
          },
          child: const Text('Knowledge Production'),
        ),
      ),
    );
  }
}
