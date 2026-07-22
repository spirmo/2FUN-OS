import time
import uuid
import traceback


from TANDIL_GOVERNANCE.core_engine.founder.condition_reactivation_engine import (
    ConditionReactivationEngine
)
from TANDIL_GOVERNANCE.core_engine.founder.founder_state_mapper import FounderStateMapper
from core.governance.schemas.event_schema import normalize_event, validate_event
from core.governance.hook_router import GovernanceHookRouter
from TANDIL_GOVERNANCE.core_engine.runtime.runtime_context import is_test_mode
from TANDIL_GOVERNANCE.constitution.core_constitution import CoreConstitution

from TANDIL_GOVERNANCE.core_engine.founder.founder_rules import FounderRules

from TANDIL_GOVERNANCE.core_engine.event_bus.async_queue import (
    AsyncQueueEngine,
)
from TANDIL_GOVERNANCE.core_engine.event_bus.event_logger import (
    EventLogger,
)
from TANDIL_GOVERNANCE.core_engine.event_bus.event_validator import (
    EventValidator,
)
from TANDIL_GOVERNANCE.core_engine.event_bus.risk_analyzer import (
    RiskAnalyzer,
)
from TANDIL_GOVERNANCE.core_engine.event_bus.conflict_resolver import (
    ConflictResolver,
)
from TANDIL_GOVERNANCE.core_engine.policy.policy_engine import (
    PolicyEngine,
)
from TANDIL_GOVERNANCE.core_engine.policy_registry.policy_registry import (
    PolicyRegistry,
)
from TANDIL_GOVERNANCE.core_engine.policy_classification.policy_classifier import (
    PolicyClassifier,
)
from TANDIL_GOVERNANCE.core_engine.policy_draft.policy_draft_engine import (
    PolicyDraftEngine,
)
from TANDIL_GOVERNANCE.core_engine.router.decision_router import (
    DecisionRouter,
)
from TANDIL_GOVERNANCE.core_engine.approval.approval_layer import (
    ApprovalLayer,
)
from TANDIL_GOVERNANCE.core_engine.enforcement.enforcement_engine import (
    EnforcementEngine,
)
from TANDIL_GOVERNANCE.core_engine.memory.memory_engine import (
    MemoryEngine,
)
from TANDIL_GOVERNANCE.core_engine.governance.governance_engine import (
    GovernanceEngine,
)
from TANDIL_GOVERNANCE.core_engine.governance.governance_history import (
    GovernanceHistory,
)
from TANDIL_GOVERNANCE.core_engine.snapshot_manager import (
    SnapshotManager,
)
from TANDIL_GOVERNANCE.core_engine.snapshot.snapshot_decider import (
    SnapshotDecider,
)
from TANDIL_GOVERNANCE.core_engine.audit.audit_engine import (
    AuditEngine,
)
from TANDIL_GOVERNANCE.core_engine.adaptive.adaptive_engine import (
    AdaptiveEngine,
)
from TANDIL_GOVERNANCE.core_engine.conflict.conflict_resolver_advanced import (
    ConflictResolverAdvanced,
)
from TANDIL_GOVERNANCE.core_engine.simulation.simulation_engine import (
    SimulationEngine,
)
from TANDIL_GOVERNANCE.core_engine.reporting.reporting_engine import (
    ReportingEngine,
)
from TANDIL_GOVERNANCE.core_engine.behavior.behavior_engine import (
    BehavioralEngine,
)
from TANDIL_GOVERNANCE.core_engine.identity.identity_engine import (
    IdentityEngine,
)
from TANDIL_GOVERNANCE.core_engine.founder.founder_store import (
    FounderStore,
)
from TANDIL_GOVERNANCE.core_engine.founder.founder_engine import (
    FounderEngine,
)
from TANDIL_GOVERNANCE.core_engine.founder.founder_cli import (
    FounderCLI,
)


class EventBus:

    REQUIRED_EVENT_FIELDS = [
        "source",
        "event_type",
        "target",
        "value",
        "event_id",
    ]

    def __init__(self):

        # =========================
        # CORE STATE
        # =========================

       # self.reactivation_engine = ConditionReactivationEngine(self.founder_store)
        self.founder_rules = FounderRules()
        self.results = {}
        self.buffer = []
        self.handlers = []
        self.subscribers = []
        self.hook_router = GovernanceHookRouter()
        # =========================
        # SNAPSHOT MANAGER
        # =========================
        self.snapshot_manager = SnapshotManager()
        self.snapshot_decider = SnapshotDecider()
        snapshot = self.snapshot_manager.load()

        if snapshot and not is_test_mode():
            self.results = snapshot.get("results", {})
            self.buffer = snapshot.get("buffer", [])
            print("[RECOVERY] Snapshot restored")
        snapshot = None

        if not is_test_mode():
            snapshot = self.snapshot_manager.load()
        # =========================
        # FOUNDATION
        # =========================
        self.constitution = CoreConstitution()
        # =========================
        # ENGINES
        # =========================
        self.policy_registry = PolicyRegistry()
        self.policy = PolicyEngine()
        self.policy_draft = PolicyDraftEngine()
        self.approval = ApprovalLayer(self.policy_registry)
        self.enforcement = EnforcementEngine(self.policy_registry)
        self.memory = MemoryEngine()
        self.governance_engine = GovernanceEngine()
        self.governance_history = GovernanceHistory()
        self.policy_classifier = PolicyClassifier()
        self.router = DecisionRouter()
        self.audit = AuditEngine()
        self.adaptive = AdaptiveEngine()
        self.conflict_advanced = ConflictResolverAdvanced()
        self.simulation = SimulationEngine()
        self.reporting = ReportingEngine()
        self.behavior = BehavioralEngine()
        self.identity = IdentityEngine()
        self.logger = EventLogger()
        self.validator = EventValidator()
        self.risk = RiskAnalyzer()
        self.conflict = ConflictResolver()
        # =========================
        # FOUNDER SYSTEM
        # =========================
        self.founder_store = FounderStore()
        self.founder_engine = FounderEngine(self.founder_store)
        self.founder_cli = FounderCLI(self.founder_engine)
        self.reactivation_engine = ConditionReactivationEngine(
            self.founder_store
        )
        # =========================
        # ASYNC
        # =========================
        self.async_queue = AsyncQueueEngine(self._process_event)

    # ==================================================
    # HELPERS
    # ==================================================
    def generate_trace_id(self):
        return str(uuid.uuid4())

    def subscribe(self, callback):
        if callback not in self.subscribers:
            self.subscribers.append(callback)
        policy_draft = event.get("policy_draft", {})
        if policy_draft.get("status") == "DRAFT_CREATED":
            self.founder_store.add(event)
            self.policy_registry.register_draft(policy_draft["draft"])
    # ==================================================
    # VALIDATION
    # ==================================================
    def validate_event_schema(self, event):
        return validate_event(event)

    # ==================================================
    # EMIT
    # ==================================================
    def emit(self, source, event_type, target, value):

        event = {
            "source": source,
            "event_type": event_type,
            "target": target,
            "value": value,
        }

        constitution_result = self.constitution.validate_action(
            source,
            event_type,
            target,
        )

        if constitution_result["status"] == "BLOCKED":
            return {
                "status": "blocked_by_constitution",
                "reason": constitution_result["reason"],
            }

        event_id = str(time.time())
        event["event_id"] = event_id

        event = normalize_event(event)

        self.results[event_id] = {
            "status": "queued",
            "event_id": event_id,
        }

        self.async_queue.push(event)

        return {
            "status": "queued",
            "event_id": event_id,
        }

    # ==================================================
    # PROCESS EVENT
    # ==================================================

    def _process_event(self, event):
        print(f"[WORKER] Processing event: {event}")

        # 1. normalize (فقط یک بار، همین اول)y7
        event = normalize_event(event)
        event_id = event.get("event_id")
        for subscriber in self.subscribers:
            subscriber(event)
        # 2. trace_id همیشه جدید
        event["trace_id"] = self.generate_trace_id()

        # 3. trace_path اگر نبود بساز، اگر بود نگه دار
        event.setdefault("trace_path", [])

        # =========================
        # AUDIT STAGE (PIPELINE)
        # =========================

        audit_result = self.audit.record(event)
        event["audit"] = audit_result
        event.setdefault("trace_path", [])
        event["trace_path"].append("audit")
        try:
            schema_check = self.validate_event_schema(event)
            if not schema_check.get("valid", False):
                self.results[event_id] = {
                    "status": "REJECTED",
                    "reason": schema_check.get("reason"),
                    "missing_fields": schema_check.get(
                        "missing_fields",
                        [],
                    ),
                }
                return
            print("[WORKER] Schema validation passed")
        except Exception as e:
            print("[WORKER ERROR]", str(e))
            traceback.print_exc()
            return
        # =========================
        # SNAPSHOT
        # =========================
        state = {
            "results": self.results.copy(),
            "buffer": list(self.buffer),
            "timestamp": time.time(),
        }
        self.snapshot_manager.save(state)
        snapshot_decision = self.snapshot_decider.should_snapshot(event)
        if snapshot_decision["take_snapshot"]:
            snapshot_payload = {
                "event": event,
                "decision": snapshot_decision,
            }
            self.snapshot_manager.save(
                snapshot_payload
            )
            # =========================
            # TARGO SNAPSHOT
            # =========================
            if (
                snapshot_decision.get("reason")
                == "targo_milestone"
            ):
                self.snapshot_manager.save_targo_snapshot(
                    event.get(
                        "event_type",
                        "UNKNOWN_TARGO"
                    ),
                    snapshot_payload
                )
            self.snapshot_decider.last_snapshot_time = time.time()
        # =========================
        # POLICY
        # =========================
        policy_result = self.policy.evaluate(event)
        event["policy"] = policy_result
        event["trace_path"].append("policy")
        if policy_result.get("status") == "BLOCKED":
            self.results[event_id] = {
                "status": "blocked",
                "policy": policy_result,
            }
            return
        # =========================
        # ENFORCEMENT
        # =========================
        enforcement_result = self.enforcement.enforce(event)
        event["enforcement"] = enforcement_result
        event["trace_path"].append("enforcement")
        # =========================
        # APPROVAL
        # =========================
        approval_result = self.approval.submit(event)
        event["approval"] = approval_result
        event["trace_path"].append("approval")
        # =========================
        # MEMORY
        # =========================
        memory_result = self.memory.record_event(event)
        event["memory"] = memory_result
        event["trace_path"].append("memory")
        # =========================
        # GOVERNANCE
        # =========================
        governance_result = self.governance_engine.evaluate(
            event,
            policy_result,
            memory_result,
        )
        event["governance"] = governance_result
        draft_result = self.policy_draft.generate(event)
        event["policy_draft"] = draft_result
        if draft_result["status"] == "DRAFT_CREATED":
            self.policy_registry.register_draft(
                draft_result["draft"]
            )
        event["trace_path"].append("governance")
        # =========================
        # POLICY DRAFT LAYER (NEW - SAFE HOOK)
        # =========================
        policy_draft = self.policy_draft.generate(event)
        event["policy_draft"] = policy_draft
        event["founder_visibility"] = {
            "policy_draft_status": policy_draft.get("status"),
            "has_policy_draft": (
                policy_draft.get("status") == "DRAFT_CREATED"
            )
        }
        # =========================
        # CLASSIFICATION
        # =========================
        classification = self.policy_classifier.classify(
            event,
            policy_result,
            memory_result,
            governance_result,
        )
        event["classification"] = classification
        # =========================
        # RULE RESOLUTION LAYER
        # =========================
        rule = self.policy_registry.find_rule(event["target"])
        rule_ui_state = rule.get("ui_state", {
            "mode": rule.get("mode", "AUTO"),
            "color": "BLUE",
            "founder_editable": False,
            "founder_notify": False
        })
        event["rule"] = rule
        event["rule_ui_state"] = rule_ui_state
        self.reactivation_engine.scan()
        return event
        # =====================
        # FIND RULE
        # =====================
        def find_rule(self, target):
            for rule in self.rules:
                if rule["target"] == target or rule["target"] == "*":

                    ui_state = self._build_ui_state(rule)

                    rule["ui_state"] = ui_state
                    return rule

            return {
                "id": "DEFAULT",
                "mode": "AUTO",
                "ui_state": {
                "mode": "AUTO",
                "color": "BLUE",
                "founder_editable": False,
                "founder_notify": False
                }
            }
        # =========================
        # DECISION
        # =========================
        founder_result = self.founder_rules.evaluate(
            event,
            policy_result,
            memory_result,
            governance_result
        )
        if founder_result["status"] == "pending_founder_approval":
            decision = founder_result
        else:
            decision = self.router.decide(
                classification,
                policy_result,
                enforcement_result,
                governance_result,
                rule,
            )

        state_mapper = FounderStateMapper()

        event["founder_state"] = state_mapper.map(
            event,
            decision,
            rule
        )
        # =========================
        # FOUNDER HOLD
        # =========================
        if decision["status"] == "pending_founder_approval":
            self.founder_store.add(event)
            print("🔥 EVENT SAVED TO FOUNDER STORE")
            self.results[event_id] = {
                "status": "pending_founder_approval",
                "policy": policy_result,
                "approval": approval_result,
                "memory": memory_result,
                "governance": governance_result,
                "event": event,
            }
            return
        # =========================
        # HARD STOP ENFORCEMENT
        # =========================
        if enforcement_result.get("status") == "BLOCKED":
            self.results[event_id] = {
                "status": "blocked_by_enforcement",
                "reason": enforcement_result.get("reason"),
                "event": event,
            }
            return
        # =========================
        # HARD STOP GOVERNANCE
        # =========================
        if governance_result["recommendation"] == "BLOCK":
            self.results[event_id] = {
                "status": "blocked_by_governance",
                "governance": governance_result,
                "event": event,
            }
            print("[GOVERNANCE] Event blocked")
            return

        # =========================
        # AUDIT (PIPELINE STAGE)
        # =========================
        audit_result = self.audit.record(event)
        event["audit"] = audit_result
        event["trace_path"].append("audit")
        # =========================
        # BUFFER
        # =========================
        self.buffer.append(event)

        # =========================
        # HOOK ROUTING LAYER
        # =========================
        self.hook_router.dispatch(event)

        # =========================
        # FINAL RESULT
        # =========================
        self.results[event_id] = {
            "status": "completed",
            "policy": policy_result,
            "approval": approval_result,
            "memory": memory_result,
            "governance": governance_result,
            "event": event,
        }
        # =========================
        # SNAPSHOT SAVE
        # =========================
        snapshot_state = {
            "event_id": event_id,
            "results": self.results,
            "buffer": self.buffer,
            "last_event": event,
        }
        self.snapshot_manager.save(snapshot_state)
        print("[WORKER] Event completed")
        # =========================
        # HANDLERS
        # =========================
        for handler in self.handlers:
            handler(event)
        return
