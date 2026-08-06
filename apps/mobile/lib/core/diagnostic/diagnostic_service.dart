import 'engine/diagnostic_engine.dart';
import 'models/diagnostic_event.dart';

import 'diagnostic_logger.dart';

import 'interfaces/diagnostic_storage.dart';
import 'interfaces/diagnostic_reporter.dart';
import 'interfaces/diagnostic_event_publisher.dart';
import 'interfaces/diagnostic_recovery.dart';


class DiagnosticService {

  final DiagnosticEngine engine;

  final DiagnosticLogger logger;

  final DiagnosticStorage? storage;

  final DiagnosticReporter? reporter;

  final DiagnosticEventPublisher? publisher;

  final DiagnosticRecovery? recovery;


  DiagnosticService({
    required this.engine,
    required this.logger,
    this.storage,
    this.reporter,
    this.publisher,
    this.recovery,
  });


  Future<void> record({

    required String source,

    required String type,

    required String severity,

    required String message,

    Map<String, dynamic>? metadata,

  }) async {


    final event = DiagnosticEvent(

      id: DateTime.now()
          .millisecondsSinceEpoch
          .toString(),

      timestamp: DateTime.now(),

      source: source,

      type: type,

      severity: severity,

      message: message,

      metadata: metadata,

    );

   final processedEvent = await engine.process(event);
     
    logger.log(processedEvent);


    await storage?.save(
      processedEvent.toMap(),
    );


  if (publisher != null) {
    await publisher!.publish(processedEvent);
  }


    await reporter?.report(
      processedEvent.toMap(),
    );


    if (await recovery?.canRecover(processedEvent) ?? false) {

      await recovery!.recover(processedEvent);

    }

  }


  List<DiagnosticEvent> getEvents(){

    return logger.events;

  }


  void clear(){

    logger.clear();

  }

}
