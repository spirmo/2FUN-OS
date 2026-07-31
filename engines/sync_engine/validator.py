class DatabaseValidator:

    def validate_tables(self, tables):

        if not tables:
            return {
                "valid": False,
                "reason": "No tables found"
            }

        return {
            "valid": True,
            "tables_count": len(tables),
            "tables": tables
        }
