import 'package:flutter/material.dart';
import '../../../../core/database/database_service.dart';
import 'package:sqflite/sqflite.dart';

class ConceptReviewPage extends StatefulWidget {
  final int conceptId;

  const ConceptReviewPage({
    super.key,
    required this.conceptId,
  });

  @override
  State<ConceptReviewPage> createState() =>
      _ConceptReviewPageState();
}

class _ConceptReviewPageState
    extends State<ConceptReviewPage> {
    List<Map<String, dynamic>> items = [];

  Future<void> _loadItems() async {
  final db = await DatabaseService.instance.database;

  final result = await db.query(
    'concept_items',
    where: 'concept_id = ?',
    whereArgs: [
      widget.conceptId,
    ],
  );

  setState(() {
    items = result;
  });
}
  @override
void initState() {
  super.initState();
  _loadItems();
}
 Future<void> _approve() async {
  final db = await DatabaseService.instance.database;

  await db.update(
    "concepts",
    {
      "status": "APPROVED",
    },
    where: "id = ?",
    whereArgs: [
      widget.conceptId,
    ],
  );

  await db.update(
    "concept_system",
    {
      "status": "APPROVED",
    },
    where: "concept_id = ?",
    whereArgs: [
      widget.conceptId,
    ],
  );

  if (!mounted) return;

  Navigator.pop(context);
}
Future<void> _reject() async {
  final db = await DatabaseService.instance.database;

  await db.update(
    "concepts",
    {
      "status": "REJECTED",
    },
    where: "id = ?",
    whereArgs: [
      widget.conceptId,
    ],
  );

  if (!mounted) return;

  Navigator.pop(context);
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text("Concept ${widget.conceptId}"),
        backgroundColor: Colors.black,
      ),
      body: Column(
  children: [

    Expanded(
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];

          return Card(
            color: Colors.grey[900],
            child: ListTile(
              title: Text(
                item["item_key"] ?? "",
                style: const TextStyle(
                  color: Colors.amber,
                ),
              ),
              subtitle: Text(
                item["item_value"] ?? "",
                style: const TextStyle(
                  color: Colors.white,
                ),
              ),
            ),
          );
        },
      ),
    ),

    Row(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [

    ElevatedButton(
      onPressed: _approve,
      child: const Text("Approve"),
    ),

    const SizedBox(width: 20),

    ElevatedButton(
      onPressed: _reject,
      child: const Text("Reject"),
    ),

  ],
),

    const SizedBox(height: 20),
        ],
      ),
    );
  }
}
