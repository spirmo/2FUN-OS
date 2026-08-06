abstract class DiagnosticStorage {
  Future<void> save(Map<String, dynamic> event);

  Future<List<Map<String, dynamic>>> load();

  Future<void> clear();
}
