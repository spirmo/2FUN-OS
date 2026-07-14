import 'package:flutter/material.dart';

import '../../../../core/database/database_service.dart';
import '../../../../core/language/language_service.dart';
import 'create_domain_page.dart';

class DomainsPage extends StatefulWidget {
  const DomainsPage({super.key});

  @override
  State<DomainsPage> createState() => _DomainsPageState();
}

class _DomainsPageState extends State<DomainsPage> {
  final LanguageService languageService = LanguageService();

  List<Map<String, dynamic>> domains = [];

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    final code = await languageService.getLanguage();
    await languageService.load(code);
    await _loadDomains();

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _loadDomains() async {
    final db = await DatabaseService.instance.database;

    domains = await db.query(
      'domains',
      orderBy: 'id ASC',
    );
  }

  String _domainName(Map<String, dynamic> domain) {
    final currentLanguage = awaitLanguage();

    switch (currentLanguage) {
      case 'fa':
        return domain["name_fa"] ?? "";
      case 'ar':
        return domain["name_ar"] ?? "";
      default:
        return domain["name_en"] ?? "";
    }
  }

  String awaitLanguage() {
    return languageService.text("app_name") == "توفان"
        ? "fa"
        : (languageService.text("continue_guest") == "الدخول كضيف"
            ? "ar"
            : "en");
  }

  Color statusColor(String status) {
    switch (status) {
      case "APPROVED":
        return Colors.amber;
      case "REJECTED":
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData statusIcon(String status) {
    switch (status) {
      case "
