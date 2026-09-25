# core/action/base.py

class BaseAction:
    def execute(self, context: dict):
        raise NotImplementedError("Action must implement execute()")
