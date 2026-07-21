import 'package:flutter/material.dart';

class GovernanceDashboardPage extends StatelessWidget {
  const GovernanceDashboardPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "2FUN Governance Dashboard",
        ),
      ),

      body: ListView(
        padding: const EdgeInsets.all(16),

        children: [

          _item(
            "Concept Approval",
          ),

          _item(
            "User Management",
          ),

          _item(
            "Content Review",
          ),

          _item(
            "Audit Reports",
          ),

        ],
      ),
    );
  }


  Widget _item(String title) {

    return Card(
      color: Colors.grey[900],

      child: ListTile(
        title: Text(
          title,
          style: const TextStyle(
            color: Colors.amber,
          ),
        ),

        trailing: const Icon(
          Icons.arrow_forward_ios,
          color: Colors.white,
        ),
      ),
    );

  }
}
