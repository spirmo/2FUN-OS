from sqlalchemy import text


class GatewayIdentityRepository:
    """
    Persistent mapping between external gateway identities
    and the universal ecosystem User.
    """

    def ensure_table(self, session):
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS user_gateway_identities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                gateway TEXT NOT NULL,
                external_id TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (gateway, external_id),
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """))

    def find_user(
        self,
        session,
        gateway: str,
        external_id: str,
    ):
        row = session.execute(text("""
            SELECT u.*
            FROM users u
            JOIN user_gateway_identities g
              ON g.user_id = u.id
            WHERE g.gateway = :gateway
              AND g.external_id = :external_id
            LIMIT 1
        """), {
            "gateway": gateway,
            "external_id": str(external_id),
        }).first()

        return row

    def link(
        self,
        session,
        user_id: int,
        gateway: str,
        external_id: str,
    ):
        session.execute(text("""
            INSERT INTO user_gateway_identities (
                user_id,
                gateway,
                external_id
            )
            VALUES (
                :user_id,
                :gateway,
                :external_id
            )
        """), {
            "user_id": user_id,
            "gateway": gateway,
            "external_id": str(external_id),
        })
        session.flush()
