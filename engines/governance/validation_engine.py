class ValidationEngine:
    """
    Responsible for validating incoming governance entities.
    """

    def validate_concept(self, concept: dict) -> dict:
        errors = []

        required_fields = [
            "title_fa",
            "definition",
            "source",
            "evidence",
        ]

        for field in required_fields:
            if not concept.get(field):
                errors.append(
                    f"Missing required field: {field}"
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }
