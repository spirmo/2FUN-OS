from platform_core.audit.audit_engine import AuditEngine


class AuditListener:

    def __init__(self):
        self.audit = AuditEngine()

    def handle(self, event, state):
        result = self.audit.record(event)

        print("[AUDIT LISTENER] RECORDED:", event.get("event_type"))

        return {
            "status": "audit_recorded",
            "result": result
        }
