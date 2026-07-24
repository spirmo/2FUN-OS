import time


class ApprovalLayer:

    def __init__(self, policy_registry):
        self.policy_registry = policy_registry
        self.queue = []
        self.approved = []
        self.rejected = []

    def submit(self, policy_draft):

        draft = {
            "id": len(self.queue) + 1,
            "policy": {
                "source": policy_draft.get("source"),
                "event_type": policy_draft.get("event_type"),
                "target": policy_draft.get("target"),
                "value": policy_draft.get("value"),
            },
            "status": "PENDING_FOUNDER_APPROVAL",
            "timestamp": time.time(),
        }

        self.queue.append(draft)

        return draft

    def approve(self, policy_id, approver="FOUNDER"):

        for item in self.queue:

            if item["id"] == policy_id:

                item["status"] = "APPROVED"
                item["approved_by"] = approver
                item["approved_at"] = time.time()

                self.approved.append(item)
                self.queue.remove(item)

                return item

        return {"status": "NOT_FOUND"}

    def founder_approve(self, policy_id, founder="FOUNDER"):

        for item in self.queue:

            if item["id"] == policy_id:

                item["status"] = "APPROVED"
                item["approved_by"] = founder
                item["approved_at"] = time.time()

                self.approved.append(item)
                self.queue.remove(item)

                return item

        return {"status": "NOT_FOUND"}

    def reject(self, policy_id, reason="NO_REASON"):

        for item in self.queue:

            if item["id"] == policy_id:

                item["status"] = "REJECTED"
                item["reason"] = reason
                item["rejected_at"] = time.time()

                self.rejected.append(item)
                self.queue.remove(item)

                return item

        return {"status": "NOT_FOUND"}

    def get_pending(self):
        return self.queue

    def get_approved(self):
        return self.approved

    def get_rejected(self):
        return self.rejected
