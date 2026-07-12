class CompletionQueue:
    """
    Stores nodes waiting for completion.
    """

    def __init__(self):
        self._queue = []

    def add(self, node):
        self._queue.append(node)
        return {
            "status": "QUEUED",
            "queue_size": len(self._queue),
        }

    def size(self):
        return len(self._queue)

    def all(self):
        return list(self._queue)
