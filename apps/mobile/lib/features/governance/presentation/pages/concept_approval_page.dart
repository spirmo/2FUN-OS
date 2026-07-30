import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../data/governance_container.dart';
import '../../domain/permission_service.dart';


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

  final repository =
      GovernanceContainer.repository;



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

      where: 'status IN (?, ?, ?)',

      whereArgs: const [
        'PENDING',
        'APPROVED',
        'REJECTED',
      ],
    );



    final enrichedConcepts =
        <Map<String, dynamic>>[];



    for (final concept in result) {

      final items =
          await db.query(
            'concept_items',

            where: 'concept_id = ?',

            whereArgs: [
              concept['id'],
            ],
          );



      final map =
          Map<String, dynamic>.from(
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


    final role =
        await DatabaseService.instance
            .getUserRole(
              "validator_test",
            );



    final canApprove =
        PermissionService.can(
          role ?? "USER",
          "concept_approve",
        );



    if (!canApprove) {

      _showMessage(
        "Permission Denied",
      );

      return;

    }



    final result =
        repository.evaluateConcept(
          concept["id"],
          concept,
        );



    if (result["approved"] == true) {


      final db =
          await DatabaseService.instance.database;



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



    _showMessage(

      result["approved"] == true

          ? "Concept Approved"

          : "Concept Rejected",

    );

  }
  Future<void> _rejectConcept(
    Map<String, dynamic> concept,
  ) async {


    final db =
        await DatabaseService.instance.database;
    await db.update(

      "concepts",

      {
        "status": "REJECTED",
      },

      where: "id = ?",

      whereArgs: [
        concept["id"],
      ],

    );
    await _loadPendingConcepts();

  }
  void _showMessage(
    String message,
  ) {

    ScaffoldMessenger.of(context)
        .showSnackBar(

      SnackBar(
        content: Text(message),
      ),

    );

  }

  @override
  Widget build(
    BuildContext context,
  ) {

    return Scaffold(

      backgroundColor:
          Colors.black,



      appBar: AppBar(

        backgroundColor:
            Colors.black,


        title:
            const Text(
              "Concept Approval",
            ),

      ),



      body:
          ListView(

            padding:
                const EdgeInsets.all(16),


            children:

                concepts.isEmpty

                    ?

                    [

                      const Center(

                        child:
                            Padding(

                              padding:
                                  EdgeInsets.only(
                                    top: 40,
                                  ),


                              child:
                                  Text(

                                    "No Pending Concepts",


                                    style:
                                        TextStyle(
                                          color:
                                              Colors.white,
                                        ),

                                  ),

                            ),

                      ),

                    ]


                    :

                    concepts
                        .map(

                          (concept) =>
                              _conceptCard(
                                concept,
                              ),

                        )
                        .toList(),

          ),

    );

  }





  Widget _conceptCard(
    Map<String, dynamic> concept,
  ) {


    final status =
        concept["status"];



    return Card(

      color:

          status == "APPROVED"

              ? Colors.green[900]

              : status == "REJECTED"

                  ? Colors.red[900]

                  : Colors.grey[900],



      child:
          Padding(

            padding:
                const EdgeInsets.all(12),


            child:
                Column(

                  crossAxisAlignment:
                      CrossAxisAlignment.start,


                  children: [

                    Text(

                      concept["name_fa"] ?? "",


                      style:
                          const TextStyle(

                            color:
                                Colors.white,

                            fontSize:
                                18,

                          ),

                    ),



                    const SizedBox(
                      height: 8,
                    ),



                    Text(

                      "STATUS = $status",


                      style:
                          TextStyle(

                            color:

                                status == "APPROVED"

                                    ? Colors.green

                                    : status == "REJECTED"

                                        ? Colors.red

                                        : Colors.amber,


                            fontSize:
                                14,


                            fontWeight:
                                FontWeight.bold,

                          ),

                    ),



                    const SizedBox(
                      height: 8,
                    ),



                    _infoText(
                      "definition",
                      concept["definition"],
                    ),



                    _infoText(
                      "source",
                      concept["source"],
                    ),



                    _infoText(
                      "evidence",
                      concept["evidence"],
                    ),



                    const SizedBox(
                      height: 12,
                    ),



                    Row(

                      children: [

                        ElevatedButton(

                          onPressed:

                              status == "PENDING"

                                  ? () async {
                                      await _approveConcept(
                                      concept,
                                    );
                                  }

                                  : null,


                          child:
                              Text(

                                status == "APPROVED"

                                    ? "Approved"

                                    : status == "REJECTED"

                                        ? "Rejected"

                                        : "Approve",

                              ),

                        ),



                        const SizedBox(
                          width: 12,
                        ),



                        ElevatedButton(

                          onPressed:

                              status == "PENDING"

                                  ? () async {
                                    await _rejectConcept(
                                    concept,
                                   );
                                }

                                  : null,


                          child:
                              const Text(
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





  Widget _infoText(
    String key,
    dynamic value,
  ) {

    return Text(

      "$key = ${value ?? ""}",


      style:
          const TextStyle(

            color:
                Colors.green,

            fontSize:
                12,

          ),

    );

  }

}
