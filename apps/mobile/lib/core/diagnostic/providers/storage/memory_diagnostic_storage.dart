import '../../interfaces/diagnostic_storage.dart';


class MemoryDiagnosticStorage implements DiagnosticStorage {

  final List<Map<String, dynamic>> _events = [];


  @override
  Future<void> save(
    Map<String, dynamic> event,
  ) async {

    _events.add(event);

  }


  @override
  Future<List<Map<String, dynamic>>> load() async {

    return List.unmodifiable(_events);

  }


  @override
  Future<void> clear() async {

    _events.clear();

  }

}
