import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';

class ConceptDetailPage extends StatefulWidget {
  final int conceptId;

  const ConceptDetailPage({
    super.key,
    required this.conceptId,
  });

  @override
  State<ConceptDetailPage> createState() =>
      _ConceptDetailPageState();
}

class _ConceptDetailPageState
    extends State<ConceptDetailPage> {

  final DatabaseService db =
      DatabaseService.instance;

  Map<String, dynamic>? concept;
  List<Map<String, dynamic>> items = [];
  Map<String, dynamic>? system;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {

    final database = await db.database;

    final c = await database.query(
      'concepts',
      where: 'id = ?',
      whereArgs: [widget.conceptId],
    );

    final i = await database.query(
      'concept_items',
      where: 'concept_id = ?',
      whereArgs: [widget.conceptId],
    );

    final s = await database.query(
      'concept_system',
      where: 'concept_id = ?',
      whereArgs: [widget.conceptId],
    );


    setState(() {

      concept = c.isNotEmpty ? c.first : null;

      items = i;

      system = s.isNotEmpty ? s.first : null;

    });
  }


  @override
  Widget build(BuildContext context) {

    if (concept == null) {

      return Scaffold(
        appBar: AppBar(
          title: const Text(
            "Concept Detail",
          ),
        ),
        body: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    }


    return Scaffold(

      appBar: AppBar(
        title: Text(
          concept!['name_fa'] ?? '',
        ),
      ),


      body: ListView(

        padding: const EdgeInsets.all(16),

        children: [

          const Text(
            "CONCEPT",
            style: TextStyle(
              fontSize:20,
              fontWeight:FontWeight.bold,
            ),
          ),

          Text(
            concept.toString(),
          ),


          const SizedBox(height:20),


          const Text(
            "CONCEPT SYSTEM",
            style: TextStyle(
              fontSize:20,
              fontWeight:FontWeight.bold,
            ),
          ),

          Text(
            system?.toString() ??
            "NO SYSTEM DATA",
          ),


          const SizedBox(height:20),


          const Text(
            "CONCEPT ITEMS",
            style: TextStyle(
              fontSize:20,
              fontWeight:FontWeight.bold,
            ),
          ),


          ...items.map(
            (item)=>Card(
              child: ListTile(
                title: Text(
                  item['item_key']
                  .toString(),
                ),

                subtitle: Text(
                  item['item_value']
                  .toString(),
                ),
              ),
            ),
          ),

        ],

      ),
    );
  }
}
