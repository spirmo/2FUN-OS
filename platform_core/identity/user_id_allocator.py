import sqlite3

from .user_id import generate_user_id


MAX_PERSONAL_CODE = 99_999_999


class UserIdAllocator:
    """
    Allocates the final 17-digit User ID.

    Personal codes are sequential per:
        country + province + county + city

    Allocation is lazy and concurrency-safe.

    When an external DB connection is supplied, the allocator
    participates in the caller's existing transaction.
    """

    def __init__(self, db_path="db/2fun.db"):
        self.db_path = db_path

    def _ensure_counter_table(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_id_counters (
                country_code INTEGER NOT NULL,
                province_code INTEGER NOT NULL,
                county_code INTEGER NOT NULL,
                city_code INTEGER NOT NULL,
                last_personal_code INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (
                    country_code,
                    province_code,
                    county_code,
                    city_code
                )
            )
        """)

    def _initialize_counter(
        self,
        conn,
        country,
        province,
        county,
        city,
    ):
        row = conn.execute("""
            SELECT MAX(
                CAST(substr(user_id, 10, 8) AS INTEGER)
            )
            FROM users
            WHERE user_id IS NOT NULL
              AND length(user_id) = 17
              AND substr(user_id, 1, 3) = ?
              AND substr(user_id, 4, 2) = ?
              AND substr(user_id, 6, 2) = ?
              AND substr(user_id, 8, 2) = ?
        """, (
            f"{country:03d}",
            f"{province:02d}",
            f"{county:02d}",
            f"{city:02d}",
        )).fetchone()

        return int(row[0] or 0)

    def allocate(
        self,
        country,
        province,
        county,
        city,
        conn=None,
    ):
        country = int(country)
        province = int(province)
        county = int(county)
        city = int(city)

        owns_connection = conn is None

        if owns_connection:
            connection = sqlite3.connect(self.db_path)
            try:
                connection.execute("BEGIN IMMEDIATE")

                result = self._allocate(
                    connection,
                    country,
                    province,
                    county,
                    city,
                )

                connection.commit()
                return result

            except Exception:
                connection.rollback()
                raise

            finally:
                connection.close()

        return self._allocate(
            conn,
            country,
            province,
            county,
            city,
        )

    def _allocate(
        self,
        conn,
        country,
        province,
        county,
        city,
    ):
        self._ensure_counter_table(conn)

        row = conn.execute("""
            SELECT last_personal_code
            FROM user_id_counters
            WHERE country_code = ?
              AND province_code = ?
              AND county_code = ?
              AND city_code = ?
        """, (
            country,
            province,
            county,
            city,
        )).fetchone()

        if row is None:
            last_code = self._initialize_counter(
                conn,
                country,
                province,
                county,
                city,
            )

            conn.execute("""
                INSERT INTO user_id_counters (
                    country_code,
                    province_code,
                    county_code,
                    city_code,
                    last_personal_code
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                country,
                province,
                county,
                city,
                last_code,
            ))
        else:
            last_code = int(row[0])

        next_code = last_code + 1

        if next_code > MAX_PERSONAL_CODE:
            raise RuntimeError(
                "Personal code capacity exhausted for this city"
            )

        conn.execute("""
            UPDATE user_id_counters
            SET last_personal_code = ?
            WHERE country_code = ?
              AND province_code = ?
              AND county_code = ?
              AND city_code = ?
        """, (
            next_code,
            country,
            province,
            county,
            city,
        ))

        user_id = generate_user_id(
            country,
            province,
            county,
            city,
            next_code,
        )

        return {
            "user_id": user_id,
            "personal_code": f"{next_code:08d}",
            "country": country,
            "province": province,
            "county": county,
            "city": city,
        }
