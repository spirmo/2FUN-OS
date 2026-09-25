import json
from datetime import datetime, timezone

from db.services.learning_loop_engine import run_learning_loop
from db.services.human_model_v2_engine import build_human_model_v2
from engines.tandil.control.control_layer_engine import execute_command
from modules.game.action.handlers.question_generator import QuestionGeneratorAction


class HookSystem:
    def __init__(self):
        self.pre_hooks = []
        self.post_hooks = []

    def register_pre(self, fn):
        self.pre_hooks.append(fn)

    def register_post(self, fn):
        self.post_hooks.append(fn)

    def run_pre(self, context):
        for hook in self.pre_hooks:
            context = hook(context)
        return context

    def run_post(self, context):
        for hook in self.post_hooks:
            context = hook(context)
        return context


def log_hook(context):
    log_entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "cmd": context.get("cmd"),
        "user_id": context.get("user_id"),
        "result": context.get("result"),
    }

    print(
        "[PIPELINE LOG]",
        json.dumps(log_entry, ensure_ascii=False),
    )

    context["logged"] = True
    return context


def drift_hook(context):
    result = context.get("control_result", {})
    decision = result.get("decision")
    user_id = context.get("user_id")

    if isinstance(decision, dict):
        actions = decision.get("actions", [])

        if "learning_loop" in actions:
            model = context.get("result", {}).get("model")

            if model:
                context["drift"] = run_learning_loop(
                    user_id,
                    model,
                )

    return context


def learning_hook(context):
    result = context.get("result", {})
    decision = result.get("decision", {})

    if decision.get("risk") == "HIGH":
        context["learning_trigger"] = "ACTIVE"

    return context


def question_hook(context):
    user_id = context.get("user_id")

    action = QuestionGeneratorAction()

    question_context = {
        "state": context.get("result", {}).get("model", {}),
        "history": context.get("question_history", []),
        "user_id": user_id,
    }

    context["next_questions"] = [
        action.execute(question_context)
    ]

    return context


class RuntimePipeline:
    def __init__(self):
        self.hooks = HookSystem()

        self.hooks.register_post(log_hook)
        self.hooks.register_post(drift_hook)
        self.hooks.register_post(learning_hook)
        self.hooks.register_post(question_hook)

    def run(self, cmd: str, payload: dict):
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dict")

        context = {
            "cmd": cmd,
            "payload": payload,
            "user_id": payload.get("user_id", 1),
            "result": None,
        }

        context = self.hooks.run_pre(context)

        control_result = execute_command(cmd, payload)
        context["control_result"] = control_result

        if cmd == "decision":
            user_id = context["user_id"]

            model = build_human_model_v2(user_id)

            context["result"] = {
                "model": model,
                "decision": control_result.get("decision"),
                "execution": control_result.get("execution"),
            }
        else:
            context["result"] = control_result

        context = self.hooks.run_post(context)

        return context


runtime_pipeline = RuntimePipeline()


def run_pipeline(cmd: str, payload: dict):
    return runtime_pipeline.run(cmd, payload)
