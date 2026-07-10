import 'package:flutter/material.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "2FUN",
          style: TextStyle(
            color: Colors.amber,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),

      body: Padding(
        padding: const EdgeInsets.all(24),

        child: Column(
          children: [

            const SizedBox(height: 20),

            const CircleAvatar(
              radius: 45,
              child: Icon(Icons.person,size:45),
            ),

            const SizedBox(height:20),

            const Text(
              "Guest User",
              style: TextStyle(
                color: Colors.white,
                fontSize:22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height:40),

            ListTile(
              leading: const Icon(Icons.menu_book,color: Colors.amber),
              title: const Text("Knowledge",style: TextStyle(color: Colors.white)),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.flag,color: Colors.amber),
              title: const Text("Missions",style: TextStyle(color: Colors.white)),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.groups,color: Colors.amber),
              title: const Text("Colony",style: TextStyle(color: Colors.white)),
              onTap: () {},
            ),

            ListTile(
              leading: const Icon(Icons.account_balance_wallet,color: Colors.amber),
              title: const Text("Wallet",style: TextStyle(color: Colors.white)),
              onTap: () {},
            ),

            const Spacer(),

            const Text(
              "2FUN MVP",
              style: TextStyle(
                color: Colors.grey,
              ),
            ),

            const SizedBox(height:20),
          ],
        ),
      ),
    );
  }
}
