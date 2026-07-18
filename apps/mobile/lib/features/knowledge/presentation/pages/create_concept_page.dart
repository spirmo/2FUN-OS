import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';


class CreateConceptPage extends StatefulWidget {

  final int topicId;


  const CreateConceptPage({

    super.key,

    required this.topicId,

  });



  @override
  State<CreateConceptPage> createState() =>
      _CreateConceptPageState();

}



class _CreateConceptPageState
    extends State<CreateConceptPage> {


  final LanguageService languageService =
      LanguageService();



  final TextEditingController faController =
      TextEditingController();


  final TextEditingController enController =
      TextEditingController();


  final TextEditingController arController =
      TextEditingController();


  final TextEditingController descriptionController =
      TextEditingController();





  @override
  void initState() {

    super.initState();

    _loadLanguage();

  }





  Future<void> _loadLanguage() async {

    final code =
        await languageService.getLanguage();


    await languageService.load(code);



    if (mounted) {

      setState(() {});

    }

  }







  Future<void> _saveConcept() async {


    await DatabaseService.instance.insertConcept(

      topicId: widget.topicId,

      fa: faController.text.trim(),

      en: enController.text.trim(),

      ar: arController.text.trim(),

      description:
          descriptionController.text.trim(),

    );



    if (!mounted) return;


    Navigator.pop(context, true);

  }







  Widget field(

    String label,

    TextEditingController controller, {

    int maxLines = 1,

  }) {


    return Padding(

      padding: const EdgeInsets.only(
        bottom: 10,
      ),


      child: TextField(

        controller: controller,

        maxLines: maxLines,


        style: const TextStyle(
          color: Colors.white,
        ),


        decoration: InputDecoration(

          labelText: label,


          labelStyle: const TextStyle(
            color: Colors.amber,
          ),


          enabledBorder:
              const OutlineInputBorder(
            borderSide:
                BorderSide(
              color: Colors.grey,
            ),
          ),


          focusedBorder:
              const OutlineInputBorder(
            borderSide:
                BorderSide(
              color: Colors.amber,
            ),
          ),

        ),

      ),

    );

  }







  @override
  Widget build(BuildContext context) {


    return Scaffold(


      backgroundColor: Colors.black,



      appBar: AppBar(

        backgroundColor: Colors.black,


        title: Text(

          languageService.text(
            "new_concept",
          ),

        ),

      ),





      body: Padding(

        padding:
            const EdgeInsets.all(16),


        child: ListView(

          children: [



            field(

              languageService.text(
                "name_fa",
              ),

              faController,

            ),





            field(

              languageService.text(
                "name_en",
              ),

              enController,

            ),





            field(

              languageService.text(
                "name_ar",
              ),

              arController,

            ),





            field(

              languageService.text(
                "description",
              ),

              descriptionController,

              maxLines: 4,

            ),






            const SizedBox(
              height: 20,
            ),





            SizedBox(

              width: double.infinity,


              child: ElevatedButton(

                onPressed:
                    _saveConcept,


                child: Text(

                  languageService.text(
                    "save",
                  ),

                ),

              ),

            ),


          ],

        ),

      ),

    );

  }







  @override
  void dispose() {


    faController.dispose();

    enController.dispose();

    arController.dispose();

    descriptionController.dispose();


    super.dispose();

  }

}
