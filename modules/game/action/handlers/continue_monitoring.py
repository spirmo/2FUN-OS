from modules.game.action.base import BaseAction


class ContinueMonitoringAction(BaseAction):
    """
    Compatibility implementation for the Legacy Game Action contract.

    Legacy de21141 explicitly treated continue_monitoring as EXECUTED,
    while its referenced Handler was absent from that baseline.
    No additional side effect is invented here.
    """

    def execute(self, context: dict):
        return {
            "action": "continue_monitoring",
            "status": "EXECUTED",
        }
