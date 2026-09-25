from db.services.action_router import execute_action


def execute_universal_actions(payload: dict):
    decision = payload.get("decision")
    actions = payload.get("actions", [])
    context = payload.get("context", {})

    executed_actions = []
    generated_questions = []

    for action in actions:
        result = execute_action(action, context)
        executed_actions.append(result)

        if action in ["learning_loop", "drift_monitoring"]:
            question = execute_action("question_shift", context)
            generated_questions.append(question)

    return {
        "decision": decision,
        "executed": executed_actions,
        "next_questions": generated_questions
    }
