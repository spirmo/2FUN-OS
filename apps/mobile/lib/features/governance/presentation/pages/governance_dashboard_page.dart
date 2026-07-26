import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../domain/governance_controller.dart';
import 'concept_approval_page.dart';

class GovernanceDashboardPage extends StatefulWidget {
  const GovernanceDashboardPage({
    super.key,
  });

  @override
  State<GovernanceDashboardPage> createState() =>
      _GovernanceDashboardPageState();
}

class _GovernanceDashboardPageState
    extends State<GovernanceDashboardPage> {

  String currentRole = "USER";

  @override
  void initState() {
    super.initState();
    _loadRole();
  }

  Future<void> _loadRole() async {

    final role = await DatabaseService.instance.getUserRole(
    "validator_test",
    );

    if (!mounted) return;

    setState(() {
      currentRole = role ?? "USER";
    });
  }

  @override
  Widget build(BuildContext context) {

    final controller = GovernanceController();

    final permissions =
        controller.permissionsForRole(currentRole);
        return Scaffold(
  backgroundColor: Colors.black,
  body: Center(
    child: Text(
      "ROLE = $currentRole\nPERMISSIONS = $permissions",
      style: const TextStyle(
        color: Colors.white,
        fontSize: 18,
          ),
          textAlign: TextAlign.center,
        ),
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
