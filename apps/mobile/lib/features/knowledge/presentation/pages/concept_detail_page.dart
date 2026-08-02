import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';

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

  final DatabaseService databaseService =
      DatabaseService.instance;

  final LanguageService languageService =
      LanguageService();

  Map<String, dynamic>? concept;

  List<Map<String, dynamic>> items = [];

  Map<String, dynamic>? system;

  String currentLanguage = 'fa';


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

    await _loadConcept();

    if (mounted) {
      setState(() {});
    }
  }



  Future<void> _loadConcept() async {

    final db =
        await databaseService.database;


    final c = await db.query(
      'concepts',
      where: 'id = ?',
      whereArgs: [
        widget.conceptId,
      ],
    );


    final i = await db.query(
      'concept_items',
      where: 'concept_id = ?',
      whereArgs: [
        widget.conceptId,
      ],
      orderBy: 'id ASC',
    );


    final s = await db.query(
      'concept_system',
      where: 'concept_id = ?',
      whereArgs: [
        widget.conceptId,
      ],
    );


    if (mounted) {

      setState(() {

        concept =
            c.isNotEmpty
                ? c.first
                : null;


        items = i;


        system =
            s.isNotEmpty
                ? s.first
                : null;

      });

    }

  }



  String _conceptName() {

    if (concept == null) {
      return '';
    }


    switch(currentLanguage){

      case 'en':
        return (concept!['name_en'] ?? '')
            .toString();


      case 'ar':
        return (concept!['name_ar'] ?? '')
            .toString();


      default:
        return (concept!['name_fa'] ?? '')
            .toString();

    }

  }




  Color _statusColor(
      String status,
  ){

    switch(status){

      case 'APPROVED':
        return Colors.amber;


      case 'REJECTED':
        return Colors.red;


      case 'PENDING':
        return Colors.orange;


      default:
        return Colors.grey;

    }

  }



  IconData _statusIcon(
      String status,
  ){

    switch(status){

      case 'APPROVED':
        return Icons.verified;


      case 'REJECTED':
        return Icons.cancel;


      default:
        return Icons.schedule;

    }

  }





  @override
  Widget build(
      BuildContext context,
  ){


    if(concept == null){

      return Scaffold(

        backgroundColor: Colors.black,

        body: const Center(
          child: CircularProgressIndicator(),
        ),

      );

    }



    final status =
        (concept!['status'] ?? 'PENDING')
            .toString();



    final completeness =
        (system?['completeness'] ?? 0)
            .toString();



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

            top:18,

            left:0,

            right:0,

            child: Center(

              child: AppLogo(

                type:
                    AppLogoType.dashboard,

              ),

            ),

          ),




          ListView(

            padding:
                const EdgeInsets.all(12),


            children: [


              const SizedBox(
                height:184,
              ),




              Card(

                color:
                    const Color(0xFF1B1B1B),


                child: ListTile(

                  leading: Icon(

                    _statusIcon(status),

                    color:
                        _statusColor(status),

                  ),


                  title: Text(

                    _conceptName(),

                    style:
                        TextStyle(

                      color:
                          _statusColor(status),

                      fontWeight:
                          FontWeight.bold,

                    ),

                  ),



                  subtitle: Text(

                    "ID: ${widget.conceptId}\n"
                    "STATUS: $status\n"
                    "COMPLETENESS: $completeness%",

                    style:
                        const TextStyle(

                      color:
                          Colors.grey,

                    ),

                  ),

                ),

              ),




              const SizedBox(
                height:12,
              ),





              _section(

                "CONCEPT SYSTEM",

                system,

              ),




              const SizedBox(
                height:12,
              ),




              const Text(

                "CONCEPT ITEMS",

                style:
                    TextStyle(

                  color:
                      Colors.white,

                  fontSize:
                      18,

                  fontWeight:
                      FontWeight.bold,

                ),

              ),



              const SizedBox(
                height:8,
              ),





              ...items.map(

                (item)=>Card(

                  color:
                      const Color(0xFF1B1B1B),


                  child: ListTile(

                    title: Text(

                      item['item_key']
                          .toString(),

                      style:
                          const TextStyle(

                        color:
                            Colors.amber,

                        fontWeight:
                            FontWeight.w600,

                      ),

                    ),



                    subtitle: Text(

                      item['item_value']
                          ?.toString()
                          .isEmpty == true

                          ? "NEED COMPLETION"

                          :

                          item['item_value']
                              .toString(),


                      style:
                          const TextStyle(

                        color:
                            Colors.grey,

                      ),

                    ),

                    trailing:

                        (item['item_value']
                                    ?.toString()
                                    .isEmpty == true)

                        ?

                        const Icon(

                          Icons.edit,

                          color:
                              Colors.orange,

                        )

                        :

                        const Icon(

                          Icons.check_circle,

                          color:
                              Colors.green,

                        ),

                  ),

                ),

              ),

            ],

          ),

        ],

      ),

    );

  }





  Widget _section(
      String title,
      Map<String,dynamic>? data,
  ){

    return Card(

      color:
          const Color(0xFF1B1B1B),


      child: Padding(

        padding:
            const EdgeInsets.all(12),


        child: Column(

          crossAxisAlignment:
              CrossAxisAlignment.start,


          children: [


            Text(

              title,

              style:
                  const TextStyle(

                color:
                    Colors.white,

                fontSize:
                    18,

                fontWeight:
                    FontWeight.bold,

              ),

            ),



            const SizedBox(
              height:8,
            ),



            Text(

              data?.toString()
              ??
              "NO DATA",

              style:
                  const TextStyle(

                color:
                    Colors.grey,

              ),

            ),

          ],

        ),

      ),

    );

  }

}
