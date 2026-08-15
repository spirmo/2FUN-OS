class EventPublisher:

    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def publish(self, event, state):
        results = []

        for listener in self.listeners:
            try:
                result = listener.handle(event, state)

                results.append({
                    "listener": listener.__class__.__name__,
                    "result": result,
                })

            except Exception as e:
                results.append({
                    "listener": listener.__class__.__name__,
                    "status": "error",
                    "error": str(e),
                })

        return results
