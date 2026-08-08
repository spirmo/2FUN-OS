import 'package:flutter/material.dart';

class TwoFunApp extends StatelessWidget {
  const TwoFunApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Center(
          child: Text('2FUN TEST'),
        ),
      ),
    );
  }
}
