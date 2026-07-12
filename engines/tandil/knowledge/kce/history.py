class HistoryManager:
    """
    Records immutable history entries.
    """

    def __init__(self):
        self._records = []

    def record(self, entry):
        self._records.append(entry)

    def all(self):
        return list(self._records)
