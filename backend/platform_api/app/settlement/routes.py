import json
import sqlite3
import uuid

from datetime import date, datetime, timedelta, timezone, time
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_user
from platform_core.universal_value.twofunc.daily_points import validated_daily_points
from platform_core.universal_value.twofunc.point_remainder import PointRemainderStore


router = APIRouter(prefix="/settlement/daily", tags=["Daily Settlement"])

DB_PATH = Path(__file__).resolve().parents[4] / "db" / "2fun.db"

ALLOWED_DESTINATIONS = frozenset({
    "Drika", "SHIR", "ΣSHIR", "2FUNC", "Drik"
})
DEFAULT_DESTINATION = "Drika"
SELECTION_START = time(22, 30)
SELECTION_END = time(23, 30)


class DestinationRequest(BaseModel):
    destination: Literal["Drika", "SHIR", "ΣSHIR", "2FUNC", "Drik"]


def utc_now():
    return datetime.now(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def connect_db():
    if not DB_PATH.is_file():
        raise HTTPException(
            status_code=503,
            detail="Central ecosystem database is unavailable",
        )

    con = sqlite3.connect(str(DB_PATH), timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout = 30000")
    return con


def authenticated_user_id(user) -> str:
    # The user ID comes from the verified access token and central users table.
    return str(user.id)


@router.post("/choice")
def select_destination(
    request: DestinationRequest,
    user=Depends(get_current_user),
):
    now = utc_now()

    if not (SELECTION_START <= now.time().replace(tzinfo=None) < SELECTION_END):
        raise HTTPException(
            status_code=409,
            detail="Destination selection is only available from 22:30 to 23:30 UTC",
        )

    user_id = authenticated_user_id(user)
    operational_date = now.date().isoformat()
    selected_at = utc_text(now)

    con = connect_db()
    try:
        con.execute("BEGIN IMMEDIATE")

        existing = con.execute(
            """
            SELECT status FROM daily_settlement_intents
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, operational_date),
        ).fetchone()

        if existing:
            con.rollback()
            raise HTTPException(
                status_code=409,
                detail="A settlement intent already exists for this operational date",
            )

        con.execute(
            """
            INSERT INTO daily_settlement_choices
                (user_id, operational_date, destination, selected_at_utc)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, operational_date) DO UPDATE SET
                destination = excluded.destination,
                selected_at_utc = excluded.selected_at_utc
            """,
            (user_id, operational_date, request.destination, selected_at),
        )
        con.commit()

        return {
            "status": "saved",
            "operational_date": operational_date,
            "destination": request.destination,
            "selected_at_utc": selected_at,
        }
    except HTTPException:
        raise
    except sqlite3.Error:
        con.rollback()
        raise HTTPException(status_code=503, detail="Unable to save settlement choice")
    finally:
        con.close()


@router.get("/choice")
def get_destination_choice(
    operational_date: str | None = None,
    user=Depends(get_current_user),
):
    now = utc_now()
    target_date = operational_date or now.date().isoformat()
    user_id = authenticated_user_id(user)

    con = connect_db()
    try:
        row = con.execute(
            """
            SELECT user_id, operational_date, destination, selected_at_utc
            FROM daily_settlement_choices
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, target_date),
        ).fetchone()

        return {
            "operational_date": target_date,
            "destination": row["destination"] if row else DEFAULT_DESTINATION,
            "selected_at_utc": row["selected_at_utc"] if row else None,
            "is_default": row is None,
        }
    except sqlite3.Error:
        raise HTTPException(status_code=503, detail="Unable to read settlement choice")
    finally:
        con.close()


@router.post("/intent")
def create_previous_day_intent(
    user=Depends(get_current_user),
):
    now = utc_now()
    operational_date = (now.date() - timedelta(days=1)).isoformat()
    user_id = authenticated_user_id(user)

    # Stable operation ID: repeated requests for the same user/day are idempotent.
    operation_id = str(uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"2FUN:daily-settlement:{user_id}:{operational_date}",
    ))

    con = connect_db()
    try:
        con.execute("BEGIN IMMEDIATE")
        existing = con.execute(
            """
            SELECT * FROM daily_settlement_intents
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, operational_date),
        ).fetchone()

        if existing:
            con.commit()
            return {
                "status": "existing",
                "settlement": dict(existing),
            }

        daily_points = validated_daily_points(
            user_id,
            date.fromisoformat(operational_date),
            connection=con,
        )
        point_result = PointRemainderStore().process_day(
            user_id=user_id,
            operational_date=date.fromisoformat(operational_date),
            daily_points=daily_points,
            connection=con,
        )

        existing = con.execute(
            """
            SELECT * FROM daily_settlement_intents
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, operational_date),
        ).fetchone()
        if existing:
            con.commit()
            return {"status": "existing", "settlement": dict(existing)}

        choice = con.execute(
            """
            SELECT destination FROM daily_settlement_choices
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, operational_date),
        ).fetchone()

        destination = choice["destination"] if choice else DEFAULT_DESTINATION
        trigger_reason = "USER_SELECTED" if choice else "AUTO_DRIKA"
        settlement_id = str(uuid.uuid4())

        con.execute(
            """
            INSERT INTO daily_settlement_intents (
                settlement_id, user_id, operational_date, destination,
                status, trigger_reason, operation_id, created_at_utc,
                metadata_json
            ) VALUES (?, ?, ?, ?, 'PENDING', ?, ?, ?, ?)
            """,
            (
                settlement_id,
                user_id,
                operational_date,
                destination,
                trigger_reason,
                operation_id,
                utc_text(now),
                json.dumps(
                    {
                        "origin": "platform_api",
                        "daily_points": str(point_result.daily_points),
                        "carry_in_points": str(point_result.carry_in_points),
                        "drika_amount": str(point_result.drika_amount),
                        "remainder_points": str(point_result.remainder_points),
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
            ),
        )
        con.commit()

        row = con.execute(
            "SELECT * FROM daily_settlement_intents WHERE settlement_id = ?",
            (settlement_id,),
        ).fetchone()

        return {
            "status": "created",
            "settlement": dict(row),
        }
    except HTTPException:
        con.rollback()
        raise
    except sqlite3.IntegrityError:
        con.rollback()
        # Another concurrent request may have created the same intent.
        row = con.execute(
            """
            SELECT * FROM daily_settlement_intents
            WHERE user_id = ? AND operational_date = ?
            """,
            (user_id, operational_date),
        ).fetchone()
        if row:
            return {"status": "existing", "settlement": dict(row)}
        raise HTTPException(status_code=409, detail="Settlement intent conflict")
    except sqlite3.Error:
        con.rollback()
        raise HTTPException(status_code=503, detail="Unable to create settlement intent")
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
