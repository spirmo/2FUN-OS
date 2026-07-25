import 'package:flutter/material.dart';

import '../../domain/governance_controller.dart';
import 'concept_approval_page.dart';

class GovernanceDashboardPage extends StatelessWidget {
  const GovernanceDashboardPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    const controller = GovernanceController();

    // موقتاً نقش را ثابت می‌گذاریم
    const currentRole = "Moderator";

    final permissions = controller.permissionsForRole(currentRole);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text("2FUN Governance Dashboard ($currentRole)"),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (permissions.contains("concept_approval"))
            _item(
              context,
              "Concept Approval",
            ),

          if (permissions.contains("user_management"))
            _item(
              context,
              "User Management",
            ),

          if (permissions.contains("content_review"))
            _item(
              context,
              "Content Review",
            ),

          if (permissions.contains("audit_reports"))
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
                builder: (_) => const ConceptApprovalPage(),
              ),
            );
          }
        },
      ),
    );
  }
}
