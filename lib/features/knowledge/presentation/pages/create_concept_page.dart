import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';


class CreateConceptPage extends StatefulWidget {

  final int topicId;


  const CreateConceptPage({
    super.key,
    required this.topicId,
  });


  @override
  State<CreateConceptPage> createState() => _CreateConceptPageState();
}



class _CreateConceptPageState extends State<CreateConceptPage> {


  final LanguageService languageService = LanguageService();



  @override
  void initState() {
    super.initState();

    _loadLanguage();
  }



  Future<void> _loadLanguage() async {

    final code = await languageService.getLanguage();

    await languageService.load(code);


    if (mounted) {

      setState(() {});

    }
  }




  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: Colors.black,


      appBar: AppBar(

        backgroundColor: Colors.black,

        title: Text(
          languageService.text("new_concept"),
        ),
      ),



      body: Center(

        child: Text(

          languageService.text("create_concept"),

          style: const TextStyle(
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}
