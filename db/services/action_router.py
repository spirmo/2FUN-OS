def execute_action(action, context):

    if action == "learning_loop":
        return {
            "action": action,
            "status": "EXECUTED",
            "impact": "KNOWLEDGE_UPDATED"
        }

    elif action == "drift_monitoring":
        return {
            "action": action,
            "status": "EXECUTED",
            "impact": "BEHAVIOR_ANALYZED"
        }

    elif action == "question_shift":
        from modules.game.action.handlers.question_generator import QuestionGeneratorAction
        return QuestionGeneratorAction().execute(context)

    return {
        "action": action,
        "status": "UNKNOWN"
    }
