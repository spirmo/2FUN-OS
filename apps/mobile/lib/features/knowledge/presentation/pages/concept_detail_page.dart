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



  Map<String,dynamic>? concept;

  Map<String,dynamic>? system;


  List<Map<String,dynamic>> items = [];


  String currentLanguage = 'fa';



  final Map<String,int> itemRewards = {


    "title_fa": 10,
    "title_en": 10,
    "title_ar": 10,


    "domain": 10,
    "category": 10,
    "canonical_meaning": 10,
    "definition": 10,
    "short_description": 10,


    "source": 10,
    "source_url": 10,
    "source_author": 10,
    "source_year": 10,
    "evidence": 10,


    "translation": 25,
    "question": 25,
    "mission": 35,

  };





  @override
  void initState(){

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



    if(mounted){

      setState((){});

    }


  }







  Future<void> _loadConcept() async {


    final db =
        await databaseService.database;



    final conceptResult =
        await db.query(

      'concepts',

      where:'id = ?',

      whereArgs:[
        widget.conceptId,
      ],

    );




    final itemResult =
        await db.query(

      'concept_items',

      where:'concept_id = ?',

      whereArgs:[
        widget.conceptId,
      ],

      orderBy:'id ASC',

    );





    final systemResult =
        await db.query(

      'concept_system',

      where:'concept_id = ?',

      whereArgs:[
        widget.conceptId,
      ],

    );




    if(!mounted) return;



    setState((){


      concept =
          conceptResult.isNotEmpty
          ? conceptResult.first
          : null;



      items =
          itemResult;



      system =
          systemResult.isNotEmpty
          ? systemResult.first
          : null;



    });



  }








  String _conceptName(){


    if(concept == null){

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






  String _itemStatus(
      Map<String,dynamic> item,
  ){


    final value =
        item['item_value']
        ?.toString()
        .trim();



    if(value == null || value.isEmpty){

      return "EMPTY";

    }



    return "PENDING";


  }






  Color _itemColor(
      String status,
  ){


    switch(status){


      case "APPROVED":

        return Colors.green;



      case "PENDING":

        return Colors.orange;



      default:

        return Colors.grey;


    }


  }







  IconData _itemIcon(
      String status,
  ){


    switch(status){


      case "APPROVED":

        return Icons.check_circle;



      case "PENDING":

        return Icons.hourglass_empty;



      default:

        return Icons.edit;


    }


  }






  int calculateCompleteness(){


    final requiredItems =
    items.where(

      (item)=>
          item['is_required'] == 1,

    ).toList();



    if(requiredItems.isEmpty){

      return 0;

    }



    int completed = 0;



    for(final item in requiredItems){


      final value =
          item['item_value']
          ?.toString()
          .trim();



      if(value != null &&
          value.isNotEmpty){

        completed++;

      }


    }




    return
      ((completed /
          requiredItems.length)
          *
          100)
          .round();


  }
  int itemReward(
      String key,
  ){

    return itemRewards[key] ?? 0;

  }





  @override
  Widget build(
      BuildContext context,
  ){


    if(concept == null){

      return Scaffold(

        backgroundColor: Colors.black,

        body: const Center(

          child:
              CircularProgressIndicator(),

        ),

      );

    }



    final status =
        (concept!['status'] ?? 'PENDING')
            .toString();



    final completeness =
        calculateCompleteness();



    return Scaffold(

      backgroundColor:
          Colors.black,



      appBar:
          AppBar(

        backgroundColor:
            Colors.black,

        elevation:
            0,

        centerTitle:
            true,

        title:
            const SizedBox.shrink(),

      ),




      body:
          Stack(

        children:[


          const Positioned(

            top:18,

            left:0,

            right:0,

            child:
                Center(

              child:
                  AppLogo(

                type:
                    AppLogoType.dashboard,

              ),

            ),

          ),




          SingleChildScrollView(

            padding:
                const EdgeInsets.fromLTRB(
                  12,
                  180,
                  12,
                  20,
                ),


            child:
                Column(

              crossAxisAlignment:
                  CrossAxisAlignment.start,


              children:[




                Card(

                  color:
                      const Color(0xFF1B1B1B),


                  child:
                      ListTile(


                    leading:
                        Icon(

                      _statusIcon(status),

                      color:
                          _statusColor(status),

                    ),



                    title:
                        Text(

                      _conceptName(),

                      style:
                          TextStyle(

                        color:
                            _statusColor(status),

                        fontWeight:
                            FontWeight.bold,

                      ),

                    ),



                    subtitle:
                        Text(

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

                  (item){


                    final key =
                        item['item_key']
                        .toString();



                    final value =
                        item['item_value']
                        ?.toString()
                        .trim();



                    final completed =
                        value != null &&
                        value.isNotEmpty;



                    final reward =
                        itemReward(key);



                    final itemStatus =
                        _itemStatus(item);



                    return Card(

                      color:
                          const Color(0xFF1B1B1B),



                      child:
                          ListTile(



                        onTap:
                            (){


                          if(!completed){

                            // مسیر ادیت آیتم بعداً متصل می‌شود

                          }


                        },




                        title:
                            Text(

                          key,

                          style:
                              const TextStyle(

                            color:
                                Colors.amber,

                            fontWeight:
                                FontWeight.w600,

                          ),

                        ),




                        subtitle:
                            Column(

                          crossAxisAlignment:
                              CrossAxisAlignment.start,


                          children:[


                            Text(

                              completed
                              ? value
                              : "NEED COMPLETION",

                              style:
                                  const TextStyle(

                                color:
                                    Colors.grey,

                              ),

                            ),




                            const SizedBox(
                              height:4,
                            ),




                            Text(

                              "REWARD: +$reward",

                              style:
                                  const TextStyle(

                                color:
                                    Colors.amber,

                                fontSize:
                                    12,

                              ),

                            ),


                          ],

                        ),





                        trailing:
                            Icon(

                          _itemIcon(
                            itemStatus,
                          ),

                          color:
                              _itemColor(
                                itemStatus,
                              ),

                        ),



                      ),

                    );


                  },


                ),


              ],

            ),


          ),


        ],


      ),


    );

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







  Widget _section(
      String title,
      Map<String,dynamic>? data,
  ){


    return Card(

      color:
          const Color(0xFF1B1B1B),


      child:
          Padding(

        padding:
            const EdgeInsets.all(12),


        child:
            Column(

          crossAxisAlignment:
              CrossAxisAlignment.start,


          children:[


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
