import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';


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


    setState(() {

      concepts = result;

    });

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

        children: [

          _conceptCard(
            context,
            "Sample Concept",
          ),

        ],
      ),
    );
  }


  Widget _conceptCard(
    BuildContext context,
    String title,
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
              title,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
              ),
            ),

            const SizedBox(
              height: 10,
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
                  width: 10,
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
