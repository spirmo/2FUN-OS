import '../../data/concept_governance_api_service.dart';
import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';

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

  final LanguageService languageService =
      LanguageService();

  final repository =
      GovernanceContainer.repository;

  final conceptApi =
      ConceptGovernanceApiService();

  List<Map<String, dynamic>> concepts = [];

  String currentLanguage = "fa";

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {

    currentLanguage =
        await languageService.getLanguage();

    await languageService.load(
      currentLanguage,
    );

    await _loadPendingConcepts();

    if (mounted) {
      setState(() {});
    }
  }
 Future<void> _loadPendingConcepts() async {

    final list =
        await conceptApi.getPendingConcepts();

    if (!mounted) return;

    setState(() {
      concepts = list;
    });
  }

  String conceptName(
    Map<String, dynamic> concept,
  ) {

    switch (currentLanguage) {

      case "en":
        return (concept["name_en"] ?? "")
            .toString();

      case "ar":
        return (concept["name_ar"] ?? "")
            .toString();

      default:
        return (concept["name_fa"] ?? "")
            .toString();
    }
  }

  Color statusColor(
    String status,
  ) {

    switch (status) {

      case "APPROVED":
        return Colors.green;

      case "REJECTED":
        return Colors.red;

      default:
        return Colors.orange;
    }
  }

  IconData statusIcon(
    String status,
  ) {

    switch (status) {

      case "APPROVED":
        return Icons.verified;

      case "REJECTED":
        return Icons.cancel;

      default:
        return Icons.schedule;
    }
  }
    Future<void> _approveConcept(
  Map<String, dynamic> concept,
) async {

  final queueId =
      concept["id"];

  final result =
      await conceptApi.approveConcept(
    queueId,
  );

  await _loadPendingConcepts();

  if (!mounted) return;

  _showMessage(
    result["status"] == "APPROVED"
        ? "Concept Approved"
        : "Approval Failed",
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
      where: "id=?",
      whereArgs: [
        concept["id"],
      ],
    );

    await _loadPendingConcepts();
  }

  void _showMessage(
    String message,
  ) {
    ScaffoldMessenger.of(context).showSnackBar(
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

      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const SizedBox.shrink(),
      ),

      body: Stack(

        children: [

          const Positioned(
            top: 18,
            left: 0,
            right: 0,
            child: Center(
              child: AppLogo(
                type: AppLogoType.dashboard,
              ),
            ),
          ),

          ListView(
            padding:
                const EdgeInsets.all(12),

            children: [

              const SizedBox(
                height: 184,
              ),

              if (concepts.isEmpty)

                const Center(
                  child: Padding(
                    padding:
                        EdgeInsets.only(
                      top: 40,
                    ),
                    child: Text(
                      "No Pending Concepts",
                      style: TextStyle(
                        color: Colors.white,
                      ),
                    ),
                  ),
                )

              else

                ...concepts.map(
                  (concept) =>
                      _conceptCard(
                    concept,
                  ),
                ),

            ],
          ),
        ],
      ),
    );
  }
  
    Widget _conceptCard(
    Map<String, dynamic> concept,
  ) {
    final status =
        (concept["status"] ?? "PENDING")
            .toString();

    final system =
        concept["system"]
            as Map<String, dynamic>?;

    final completeness =
        (system?["completeness"] ?? 0)
            .toString();

    return Card(
      color: const Color(0xFF1B1B1B),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [

            Row(
              children: [

                Icon(
                  statusIcon(status),
                  color:
                      statusColor(status),
                ),

                const SizedBox(width: 8),

                Expanded(
                  child: Text(
                    conceptName(concept),
                    style:
                        TextStyle(
                      color:
                          statusColor(status),
                      fontSize: 18,
                      fontWeight:
                          FontWeight.bold,
                    ),
                  ),
                ),

                Text(
                  "$completeness%",
                  style:
                      const TextStyle(
                    color:
                        Colors.amber,
                    fontWeight:
                        FontWeight.bold,
                  ),
                ),

              ],
            ),

            const SizedBox(height: 10),

            _infoText(
              "Definition",
              concept["definition"],
            ),

            _infoText(
              "Source",
              concept["source"],
            ),

            _infoText(
              "Evidence",
              concept["evidence"],
            ),

            _infoText(
              "Category",
              concept["category"],
            ),

            _infoText(
              "Canonical",
              concept["canonical_meaning"],
            ),

            const SizedBox(height: 12),

            Row(
              children: [

                Expanded(
                  child:
                      ElevatedButton(
                    onPressed:
                        status ==
                                "PENDING"
                            ? () async {
                                await _approveConcept(
                                  concept,
                                );
                              }
                            : null,
                    child:
                        Text(
                      status ==
                              "APPROVED"
                          ? "Approved"
                          : "Approve",
                    ),
                  ),
                ),

                const SizedBox(width: 12),

                Expanded(
                  child:
                      ElevatedButton(
                    onPressed:
                        status ==
                                "PENDING"
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
                ),

              ],
            ),

          ],
        ),
      ),
    );
  }

  Widget _infoText(
    String title,
    dynamic value,
  ) {
    return Padding(
      padding:
          const EdgeInsets.only(
        bottom: 6,
      ),
      child: Text(
        "$title : ${value ?? "-"}",
        style: const TextStyle(
          color: Colors.grey,
          fontSize: 13,
        ),
      ),
    );
  }
}
