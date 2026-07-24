import threading
from queue import Queue, Empty


class AsyncQueueEngine:

    def __init__(self, worker_callback):

        self.queue = Queue()
        self.worker_callback = worker_callback
        self.running = True

        self.thread = threading.Thread(target=self._worker, daemon=True)

        self.thread.start()

    def push(self, event):

        self.queue.put(event)

    def _worker(self):

        while self.running:

            try:
                event = self.queue.get(timeout=1)

                self.worker_callback(event)

                self.queue.task_done()

            except Empty:
                continue

            except Exception as e:

                print(f"[WORKER ERROR] {e}")

                import traceback
                traceback.print_exc()

                continue

    def stop(self):

        self.running = False
