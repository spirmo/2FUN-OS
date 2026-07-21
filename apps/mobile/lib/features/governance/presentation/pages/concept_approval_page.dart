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

    if (!mounted) return;

    setState(() {
      concepts = result;
    });
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

      margin: const EdgeInsets.only(
        bottom: 12,
      ),

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
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 12,
            ),

            Row(
              children: [

                ElevatedButton(
                  onPressed: () {},

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
