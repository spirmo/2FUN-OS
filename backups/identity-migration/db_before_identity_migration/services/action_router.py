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
        return {
            "action": action,
            "status": "EXECUTED",
            "impact": "DOMAIN_ROTATED"
        }

    return {
        "action": action,
        "status": "UNKNOWN"
    }
