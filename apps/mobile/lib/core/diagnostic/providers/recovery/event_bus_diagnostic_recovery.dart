import '../../models/diagnostic_event.dart';
import '../../interfaces/diagnostic_recovery.dart';


class EventBusDiagnosticRecovery
    implements DiagnosticRecovery {


  @override
  Future<bool> canRecover(
    DiagnosticEvent event,
  ) async {

    return event.severity == "CRITICAL" ||
           event.type.contains("CRASH");

  }


  @override
  Future<void> recover(
    DiagnosticEvent event,
  ) async {


    print(
      "[RECOVERY] Handling diagnostic event: ${event.type}"
    );


    // فعلا فقط ثبت recovery
    // بعدا اینجا:
    // restart service
    // rollback
    // snapshot restore
    // cache repair
    // قرار می‌گیرد


  }

}
