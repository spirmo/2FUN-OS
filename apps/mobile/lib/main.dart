import 'package:flutter/material.dart';

import 'features/auth/presentation/pages/login_page.dart';

void main() {
  runApp(const TwoFunApp());
}

class TwoFunApp extends StatelessWidget {
  const TwoFunApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
    );
  }
}
