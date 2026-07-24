class FounderCLI:

    def __init__(self, founder_engine):
        self.engine = founder_engine

    def list(self):
        queue = self.engine.pending()
        return {"count": len(queue), "queue": queue}

    def approve(self, event_id):
        return self.engine.approve(event_id)

    def veto(self, event_id):
        return self.engine.veto(event_id)
