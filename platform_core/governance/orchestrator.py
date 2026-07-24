class GovernanceOrchestrator:

    def __init__(self, policy, approval, governance, memory, audit, snapshot):
        self.policy = policy
        self.approval = approval
        self.governance = governance
        self.memory = memory
        self.audit = audit
        self.snapshot = snapshot

    def process(self, event):

        # 1. Policy
        policy_result = self.policy.evaluate(event)
        event["policy"] = policy_result

        if policy_result.get("status") == "BLOCKED":
            return self._finalize(event)

        # 2. Enforcement (if exists)
        if hasattr(self, "enforcement"):
            enforce_result = self.enforcement.enforce(event)
            event["enforcement"] = enforce_result

            if enforce_result.get("status") == "BLOCKED":
                return self._finalize(event)

        # 3. Approval
        approval_result = self.approval.submit(event)
        event["approval"] = approval_result

        # 4. Governance
        governance_result = self.governance.evaluate(
            event, policy_result, self.memory.load_last()
        )
        event["governance"] = governance_result

        # 5. Memory
        memory_result = self.memory.record_event(event)
        event["memory"] = memory_result

        # 6. Audit
        audit_result = self.audit.record(event)
        event["audit"] = audit_result

        # 7. Snapshot (optional)
        if self._should_snapshot(event):
            self.snapshot.save(event)

        return self._finalize(event)

    def _should_snapshot(self, event):
        return True  # بعداً شرطی می‌کنیم

    def _finalize(self, event):
        return {"status": "completed", "event": event}
