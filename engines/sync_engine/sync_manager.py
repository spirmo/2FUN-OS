from .concept_mapper import ConceptMapper
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
        self.mapper = ConceptMapper(
            source_db,
            target_db
        )

    def prepare_sync(self):

        tables = self.importer.get_tables()

        validation = self.validator.validate_tables(
            tables
        )

        return {
            "validation": validation,
            "ready": validation["valid"]
        }
    def sync_mobile_to_ecosystem(self):

        source = self.importer.connect()
        cursor = source.cursor()

        cursor.execute(
            """
            SELECT 
                code,
                name_fa,
                description
            FROM concepts
            WHERE status='PENDING'
            """
        )

        rows = cursor.fetchall()

        source.close()


        concepts = []

        for row in rows:
            concepts.append(
                {
                    "code": row[0],
                    "title": row[1],
                    "description": row[2] or "",
                    "domain": "GENERAL_KNOWLEDGE"
                }
            )


        result = self.merger.merge_concepts(
            concepts
        )

        return result
