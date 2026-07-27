import '../../domain/permission_service.dart';
import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../data/governance_container.dart';

class ConceptApprovalPage extends StatefulWidget {
  const ConceptApprovalPage({
    super.key,
  });

  @override
  State<ConceptApprovalPage> createState() =>
      _ConceptApprovalPageState();
}

class _ConceptApprovalPageState
    extends State<ConceptApprovalPage> {

  List<Map<String, dynamic>> concepts = [];

  final repository = GovernanceContainer.repository;

  @override
  void initState() {
    super.initState();
    _loadPendingConcepts();
  }

  Future<void> _loadPendingConcepts() async {
  final db =
      await DatabaseService.instance.database;

  final result = await db.query(
    'concepts',
    where: 'status = ?',
    whereArgs: [
      'PENDING',
    ],
  );

  final enrichedConcepts = <Map<String, dynamic>>[];

  for (final concept in result) {

    final items = await db.query(
      'concept_items',
      where: 'concept_id = ?',
      whereArgs: [
        concept['id'],
      ],
    );

    final map = Map<String, dynamic>.from(
      concept,
    );

    for (final item in items) {
      map[item['item_key'] as String] =
          item['item_value'];
    }

    enrichedConcepts.add(map);
  }

  if (!mounted) return;

  setState(() {
    concepts = enrichedConcepts;
  });
}
    

  Future<void> _approveConcept(
    Map<String, dynamic> concept,
  ) async {

    final role = await DatabaseService.instance.getUserRole(
  "validator_test",
);

final canApprove =
    PermissionService.can(
      role ?? "USER",
      "concept_approve",
    );

if (!canApprove) {
  ScaffoldMessenger.of(context)
      .showSnackBar(
        const SnackBar(
          content: Text(
            "Permission Denied",
          ),
        ),
      );

  return;
}
    print("CONCEPT DATA = $concept");
    final result = repository.evaluateConcept(
   concept["id"],
   concept,
 );

 if (result["approved"] == true) {
   final db = await DatabaseService.instance.database;

    await db.update(
      "concepts",
     {
       "status": "APPROVED",
     },
     where: "id = ?",
     whereArgs: [
       concept["id"],
     ],
   );

   await _loadPendingConcepts();
  }

    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          result["approved"]
              ? "Concept Approved"
              : "Concept Rejected",
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      backgroundColor: Colors.black,

      appBar: AppBar(
         backgroundColor: Colors.black,
        title: const Text(
          "Concept Approval",
        ),
      ),

      body: ListView(
        padding: const EdgeInsets.all(16),

        children: concepts.isEmpty
            ? [
                const Center(
                  child: Padding(
                    padding: EdgeInsets.only(
                      top: 40,
                    ),
                    child: Text(
                      "No Pending Concepts",
                      style: TextStyle(
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
              ]
            : concepts.map((concept) {

                return _conceptCard(
                  context,
                  concept,
                );

              }).toList(),
      ),
    );
  }

  Widget _conceptCard(
    BuildContext context,
    Map<String, dynamic> concept,
  ) {

    return Card(
      color: Colors.grey[900],

      child: Padding(
        padding: const EdgeInsets.all(12),

        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          children: [

            Text(
              concept["name_fa"] ?? "",
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
              ),
            ),

            Row(
              children: [

                ElevatedButton(
                  onPressed: () {
                    _approveConcept(concept);
                  },
                  child: const Text(
                    "Approve",
                  ),
                ),

                const SizedBox(
                  width: 12,
                ),

                ElevatedButton(
                  onPressed: () {},
                  child: const Text(
                    "Reject",
                  ),
                ),

              ],
            ),

          ],
        ),
      ),
    );
  }
}
