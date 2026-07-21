import 'package:flutter/material.dart';

class GovernanceLoginPage extends StatelessWidget {
  const GovernanceLoginPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "2FUN Governance Login",
        ),
      ),

      body: Center(
        child: ElevatedButton(
          onPressed: () {

          },

          child: const Text(
            "Enter Governance",
          ),
        ),
      ),
    );
  }
}
