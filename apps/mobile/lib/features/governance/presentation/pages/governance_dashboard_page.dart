import 'package:flutter/material.dart';

import 'concept_approval_page.dart';

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
            context,
            "Concept Approval",
          ),

          _item(
            context,
            "User Management",
          ),

          _item(
            context,
            "Content Review",
          ),

          _item(
            context,
            "Audit Reports",
          ),

        ],
      ),
    );
  }


  Widget _item(
    BuildContext context,
    String title,
  ) {

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

        onTap: () {

          if (title == "Concept Approval") {

            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) =>
                    const ConceptApprovalPage(),
              ),
            );

          }

        },

      ),
    );
  }
}
