import os
RUNTIME_MODE = os.getenv("TANDIL_MODE", "production")

_GLOBAL_EVENT_BUS = None

def get_event_bus():
    global _GLOBAL_EVENT_BUS

    if _GLOBAL_EVENT_BUS is None:
        from platform_core.event_bus.event_bus import EventBus
        _GLOBAL_EVENT_BUS = EventBus()   # 👈 این خط مهمه

    return _GLOBAL_EVENT_BUS

def is_test_mode():
    return RUNTIME_MODE == "test"
