# core/action/engine.py

from modules.game.action.registry import ACTION_REGISTRY

def execute_actions(decision_result: dict):

    actions = decision_result.get("actions", [])

    executed = []

    context = decision_result

    for action_name in actions:

        action = ACTION_REGISTRY.get(action_name)

        if action:
            result = action.execute(context)
            executed.append(result)
        else:
            executed.append({
                "action": action_name,
                "status": "UNKNOWN_ACTION"
            })

    return {
        "executed": executed
    }
