"""
2FUN / توفان
TANDIL Control Layer

The Control Layer is an orchestration boundary.
It coordinates TANDIL engines and Game execution.

Control does not own:
- Human Model implementation
- Cognition implementation
- Game Action implementation
- Governance authority
"""

from db.services.human_model_v2_engine import build_human_model_v2
from engines.tandil.cognition.cognitive_decision_engine import (
    evaluate_cognitive_state,
)
from engines.tandil.evolution.human_evolution_engine import (
    build_evolution_model,
)
from modules.game.entry import run_game


def execute_command(cmd: str, payload: dict | None = None):
    """
    Execute a TANDIL Control command.

    Supported commands:
        status
        human_model
        evolution
        decision
    """
    if payload is None:
        payload = {}

    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    user_id = payload.get("user_id", 1)

    if cmd == "status":
        return {
            "status": "ONLINE",
            "system": "TANDIL",
            "layer": "CONTROL_LAYER_ACTIVE",
        }

    if cmd == "human_model":
        return build_human_model_v2(user_id)

    if cmd == "evolution":
        model = build_human_model_v2(user_id)
        return build_evolution_model(model)

    if cmd == "decision":
        model = build_human_model_v2(user_id)
        decision = evaluate_cognitive_state(model)
        execution = run_game(decision)

        return {
            "decision": decision,
            "execution": execution,
        }

    return {
        "error": "UNKNOWN_COMMAND",
        "cmd": cmd,
    }
