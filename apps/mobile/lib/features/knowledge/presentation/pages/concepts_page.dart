import 'create_concept_page.dart';
import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';


class ConceptsPage extends StatefulWidget {

  final int topicId;
  final String topicName;

  const ConceptsPage({
    super.key,
    required this.topicId,
    required this.topicName,
  });


  @override
  State<ConceptsPage> createState() => _ConceptsPageState();

}



class _ConceptsPageState extends State<ConceptsPage> {


  final LanguageService languageService = LanguageService();


  List<Map<String, dynamic>> concepts = [];


  String currentLanguage = 'fa';



  @override
  void initState() {

    super.initState();

    _loadLanguage();

    _loadConcepts();

  }



  Future<void> _loadConcepts() async {

    final db = await DatabaseService.instance.database;


    final result = await db.query(

      'concepts',

      where: 'topic_id=?',

      whereArgs: [

        widget.topicId,

      ],

      orderBy: 'id ASC',

    );


    if (mounted) {

      setState(() {

        concepts = result;

      });

    }

  }





  Future<void> _loadLanguage() async {


    final code = await languageService.getLanguage();


    currentLanguage = code;


    await languageService.load(code);



    if (mounted) {

      setState(() {});

    }

  }




  String conceptName(
    Map<String, dynamic> concept,
  ) {


    switch (currentLanguage) {


      case 'en':

        return concept["name_en"].toString();



      case 'ar':

        return concept["name_ar"].toString();



      default:

        return concept["name_fa"].toString();

    }

  }




  @override
  Widget build(BuildContext context) {


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

            padding: const EdgeInsets.all(12),


            children: [


              const SizedBox(

                height: 184,

              ),




              SizedBox(

                width: double.infinity,

                height: 46,

                child: ElevatedButton.icon(


                  icon: const Icon(

                    Icons.add_circle_outline,

                  ),



                  label: Text(

                    languageService.text(

                      "new_concept",

                    ),

                  ),



                  onPressed: () async {


                    await Navigator.push(

                      context,

                      MaterialPageRoute(

                        builder: (_) => CreateConceptPage(

                          topicId: widget.topicId,

                        ),

                      ),

                    );


                    _loadConcepts();


                  },


                ),

              ),




              const SizedBox(

                height: 12,

              ),




              ...concepts.map(


                (c) => Card(

                  color: const Color(0xFF1B1B1B),


                  child: ListTile(


                    title: Text(

                      conceptName(c),


                      style: const TextStyle(

                        color: Colors.white,

                      ),

                    ),



                    subtitle: Text(

                      c["name_en"].toString(),


                      style: const TextStyle(

                        color: Colors.grey,

                      ),

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

}
