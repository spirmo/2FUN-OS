import 'governance_dashboard_page.dart';
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
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (_) =>
                    const GovernanceDashboardPage(),
              ),
            );
          },

          child: const Text(
            "Enter Governance",
          ),
        ),
      ),
    );
  }
}
