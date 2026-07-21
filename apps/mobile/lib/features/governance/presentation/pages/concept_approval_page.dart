import 'package:flutter/material.dart';

class ConceptApprovalPage extends StatelessWidget {
  const ConceptApprovalPage({
    super.key,
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
