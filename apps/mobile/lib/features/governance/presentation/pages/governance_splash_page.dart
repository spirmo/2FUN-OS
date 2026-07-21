import 'package:flutter/material.dart';

class GovernanceSplashPage extends StatelessWidget {
  const GovernanceSplashPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Text(
          "2FUN Governance",
          style: TextStyle(
            color: Colors.amber,
            fontSize: 24,
          ),
        ),
      ),
    );
  }
}
