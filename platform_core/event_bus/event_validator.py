class EventValidator:

    REQUIRED_FIELDS = ["source", "event_type", "target", "value"]

    ALLOWED_SOURCES = ["HUMAN", "MACHINE"]

    def validate(self, event):

        for field in self.REQUIRED_FIELDS:

            if field not in event:
                return {"valid": False, "reason": f"missing_field:{field}"}

        if event["source"] not in self.ALLOWED_SOURCES:
            return {"valid": False, "reason": "invalid_source"}

        return {"valid": True, "reason": "passed"}
