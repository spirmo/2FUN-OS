import 'package:flutter/material.dart';

import '../../../../core/language/language_service.dart';
import '../../../../shared/widgets/app_logo.dart';
import '../../../language/presentation/pages/language_page.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
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

  Widget menuItem({
    required IconData icon,
    required String title,
    VoidCallback? onTap,
  }) {
    final enabled = onTap != null;

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 1),
      color: const Color(0xFF1B1B1B),
      child: SizedBox(
        height: 46,
        child: ListTile(
          dense: true,
          minLeadingWidth: 0,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 12,
            vertical: 0,
          ),
          leading: Icon(
            icon,
            size: 20,
            color: enabled ? Colors.amber : Colors.grey,
          ),
          trailing: Icon(
            Icons.chevron_right,
            size: 20,
            color: enabled ? Colors.amber : Colors.grey,
          ),
          title: Text(
            title,
            style: TextStyle(
              color: enabled ? Colors.white : Colors.grey,
              fontSize: 15,
            ),
          ),
          onTap: onTap,
        ),
      ),
    );
  }

   @override
 Widget build(BuildContext context) {
   return Scaffold(
     backgroundColor: Colors.black,
     appBar: AppBar(
       automaticallyImplyLeading: false,
       backgroundColor: Colors.black,
       elevation: 0,
       centerTitle: true,
       title: const SizedBox.shrink(),
       actions: [
         IconButton(
           icon: const Icon(
             Icons.language,
            size: 20,
           ),
           onPressed: () {
             Navigator.push(
              context,
               MaterialPageRoute(
                 builder: (_) => const LanguagePage(),
               ),
             );
           },
         ),
       ],
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
             const SizedBox(height: 184),

             const CircleAvatar(
               radius: 38,
               backgroundColor: Colors.amber,
               child: Icon(
                 Icons.person,
                 size: 38,
                 color: Colors.black,
               ),
             ),

             const SizedBox(height: 12),

             Center(
               child: Text(
                 languageService.text("continue_guest"),
                 style: const TextStyle(
                   color: Colors.white,
                   fontSize: 18,
                   fontWeight: FontWeight.bold,
                 ),
               ),
             ),

             const SizedBox(height: 14),

             menuItem(
               icon: Icons.psychology,
               title: languageService.text("knowledge_injection"),
               onTap: () {
                 Navigator.pushNamed(
                   context,
                   '/knowledge-dashboard',
                 );
               },
             ),

             menuItem(
               icon: Icons.menu_book,
               title: languageService.text("knowledge"),
             ),

             menuItem(
               icon: Icons.flag,
               title: languageService.text("missions"),
             ),

             menuItem(
               icon: Icons.groups,
               title: languageService.text("colony"),
             ),

             menuItem(
               icon: Icons.account_balance_wallet,
               title: languageService.text("wallet"),
             ),

             menuItem(
               icon: Icons.settings,
               title: languageService.text("settings"),
             ),

             const SizedBox(height: 14),

             Center(
               child: Text(
                 languageService.text("app_name"),
                 style: const TextStyle(
                   color: Colors.grey,
                   fontSize: 12,
                 ),
               ),
             ),

             const SizedBox(height: 2),

             Center(
               child: Text(
                 languageService.text("version"),
                 style: const TextStyle(
                   color: Colors.grey,
                   fontSize: 11,
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

