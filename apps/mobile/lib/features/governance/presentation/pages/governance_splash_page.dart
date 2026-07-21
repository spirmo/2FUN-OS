import 'package:flutter/material.dart';

import 'governance_login_page.dart';

class GovernanceSplashPage extends StatelessWidget {
  const GovernanceSplashPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,

      body: Center(
        child: GestureDetector(
          onTap: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (_) =>
                    const GovernanceLoginPage(),
              ),
            );
          },

          child: const Text(
            "2FUN Governance",
            style: TextStyle(
              color: Colors.amber,
              fontSize: 24,
            ),
          ),
        ),
      ),
    );
  }
}
