from db.repositories.completion_queue_repository import CompletionQueueRepository
from db.repositories.concept_version_repository import ConceptVersionRepository


class KnowledgeListener:

    def __init__(self):
        self.completion_repository = CompletionQueueRepository()
        self.concept_repository = ConceptVersionRepository()


    def handle(self, event, state):

        if event.get("event_type") not in (
            "CONCEPT_APPROVED",
            "CONCEPT_PUBLISHED",
        ):
            return {
                "status": "ignored"
        }

        value = event.get("value", {})

        concept_id = value.get("concept_id")
        concept_code = value.get("concept_code")
        completeness = value.get("completeness", 0)

        result = {
            "concept_id": concept_id,
            "concept_code": concept_code,
            "completeness": completeness,
        }

        # 36 آیتم تایید شده = Concept کامل
        if completeness >= 36:
            result["status"] = "COMPLETE"
            result["knowledge_ready"] = True
            result["published"] = (
                event.get("event_type") == "CONCEPT_PUBLISHED"
            )

        # 11 تا 35 آیتم تایید شده = Concept ناقص ولی قابل استفاده
        elif completeness >= 11:

            result["status"] = "INCOMPLETE"
            result["knowledge_ready"] = True

            queue_result = self.completion_repository.add(
                concept_id=concept_id,
                concept_code=concept_code,
                completeness=completeness,
            )

            result["completion_queue"] = True
            result["queue"] = queue_result


        # کمتر از 11 آیتم
        else:

            result["status"] = "NOT_READY"
            result["knowledge_ready"] = False


        return result
