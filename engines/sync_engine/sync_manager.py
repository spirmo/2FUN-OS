from .importer import DatabaseImporter
from .validator import DatabaseValidator
from .conflict_resolver import ConflictResolver
from .merger import DatabaseMerger


class SyncManager:

    def __init__(self, source_db, target_db):

        self.importer = DatabaseImporter(source_db)
        self.validator = DatabaseValidator()
        self.conflict_resolver = ConflictResolver()
        self.merger = DatabaseMerger(target_db)


    def prepare_sync(self):

        tables = self.importer.get_tables()

        validation = self.validator.validate_tables(
            tables
        )

        return {
            "validation": validation,
            "ready": validation["valid"]
        }
