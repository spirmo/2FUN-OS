"""
2FUN Game Entry Point

Single entry boundary for all Game channels.

Channels such as Telegram, Super App and Website must call
this boundary instead of implementing Game logic themselves.
"""

from modules.game.action.engine import execute_actions


def run_game(decision: dict) -> dict:
    """
    Execute Game logic through the migrated Game Action Engine.
    """
    if not isinstance(decision, dict):
        raise TypeError("decision must be a dict")

    return execute_actions(decision)
