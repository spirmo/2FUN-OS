import sqlite3
import json
import time


class FounderStore:

    def __init__(self, db_path="founder_queue.db"):

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS founder_queue (
            event_id TEXT PRIMARY KEY,
            status TEXT,
            created_at REAL,
            payload TEXT
        )
        """)

        self.conn.commit()

    def add(self, event):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO founder_queue
        (event_id, status, created_at, payload)
        VALUES (?, ?, ?, ?)
        """, (
            event["event_id"],
            "PENDING",
            time.time(),
            json.dumps(event)
        ))

        self.conn.commit()

    def list(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT payload FROM founder_queue
        WHERE status='PENDING'
        ORDER BY created_at ASC
        """)

        rows = cursor.fetchall()

        return [json.loads(r[0]) for r in rows]

    def list_all(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT event_id, status, payload
            FROM founder_queue
            ORDER BY created_at ASC
        """)

        rows = cursor.fetchall()

        result = []
        for event_id, status, payload in rows:
            event = json.loads(payload)

            # 🔥 تنها truth
            event["status"] = status

            result.append(event)

        return result

    def approve(self, event_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE founder_queue
        SET status='APPROVED'
        WHERE event_id=?
        """, (event_id,))

        self.conn.commit()

    def remove(self, event_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        DELETE FROM founder_queue
        WHERE event_id=?
        """, (event_id,))

        self.conn.commit()
    # =========================
    # UPDATE STATUS
    # =========================
    def update_status(self, event_id, status):

        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE founder_queue
        SET status=?
        WHERE event_id=?
        """, (status, event_id))

        self.conn.commit()

    # =========================
    # APPROVED LIST
    # =========================
    def list_approved(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT payload FROM founder_queue
        WHERE status='APPROVED'
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        return [json.loads(r[0]) for r in rows]

    # =========================
    # REJECTED LIST
    # =========================
    def list_rejected(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT payload FROM founder_queue
        WHERE status='REJECTED'
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        return [json.loads(r[0]) for r in rows]

    # =========================
    # WAITING FOR CONDITION
    # =========================
    def list_waiting(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT payload FROM founder_queue
        WHERE status='WAITING_FOR_CONDITION'
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        return [json.loads(r[0]) for r in rows]
    # =========================
    # UPDATE EVENT PAYLOAD
    # =========================
    def update_event(self, event):

        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE founder_queue
        SET payload=?
        WHERE event_id=?
        """, (
            json.dumps(event),
            event["event_id"]
        ))

        self.conn.commit()

