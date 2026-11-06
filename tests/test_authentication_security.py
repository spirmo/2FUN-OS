import hashlib
import hmac
import json
import unittest
from types import SimpleNamespace
from urllib.parse import urlencode
from unittest.mock import Mock, patch

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import routes
from app.auth import dependencies


class TelegramInitDataTests(unittest.TestCase):
    def setUp(self):
        self.bot_token = "test-bot-token"
        self.fixed_now = 1800000000

        self.token_patch = patch.object(routes, "BOT_TOKEN", self.bot_token)
        self.time_patch = patch.object(
            routes.time, "time", return_value=self.fixed_now
        )
        self.token_patch.start()
        self.time_patch.start()

        self.addCleanup(self.token_patch.stop)
        self.addCleanup(self.time_patch.stop)

    def build_init_data(self, auth_date=None):
        fields = {
            "auth_date": str(
                self.fixed_now if auth_date is None else auth_date
            ),
            "query_id": "test-query-123",
            "user": json.dumps(
                {"id": 123456, "username": "test_user"},
                separators=(",", ":"),
            ),
        }

        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(fields.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            self.bot_token.encode(),
            hashlib.sha256,
        ).digest()

        signature = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        fields["hash"] = signature
        return urlencode(fields)

    def test_valid_init_data_returns_telegram_identity(self):
        result = routes.validate_telegram_init_data(
            self.build_init_data()
        )

        self.assertEqual(result["telegram_id"], 123456)
        self.assertEqual(result["username"], "test_user")

    def test_tampered_init_data_is_rejected(self):
        init_data = self.build_init_data().replace(
            "test-query-123", "tampered-query"
        )

        with self.assertRaises(HTTPException) as context:
            routes.validate_telegram_init_data(init_data)

        self.assertEqual(context.exception.status_code, 401)

    def test_expired_init_data_is_rejected(self):
        init_data = self.build_init_data(
            auth_date=self.fixed_now - 601
        )

        with self.assertRaises(HTTPException) as context:
            routes.validate_telegram_init_data(init_data)

        self.assertEqual(context.exception.status_code, 401)

    def test_duplicate_fields_are_rejected(self):
        init_data = self.build_init_data() + "&auth_date=1800000000"

        with self.assertRaises(HTTPException) as context:
            routes.validate_telegram_init_data(init_data)

        self.assertEqual(context.exception.status_code, 401)


class CurrentUserAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test-access-token",
        )

    def test_valid_token_returns_active_user(self):
        user = SimpleNamespace(
            id=7,
            active=1,
            status="ACTIVE",
        )
        self.db.query.return_value.filter.return_value.first.return_value = user

        with patch.object(
            dependencies, "verify_token", return_value={"sub": "7"}
        ):
            result = dependencies.get_current_user(
                credentials=self.credentials,
                db=self.db,
            )

        self.assertIs(result, user)

    def test_invalid_token_returns_401(self):
        with patch.object(
            dependencies,
            "verify_token",
            side_effect=ValueError("invalid token"),
        ):
            with self.assertRaises(HTTPException) as context:
                dependencies.get_current_user(
                    credentials=self.credentials,
                    db=self.db,
                )

        self.assertEqual(context.exception.status_code, 401)

    def test_missing_credentials_returns_401(self):
        with self.assertRaises(HTTPException) as context:
            dependencies.get_current_user(
                credentials=None,
                db=self.db,
            )

        self.assertEqual(context.exception.status_code, 401)

    def test_inactive_user_returns_403(self):
        user = SimpleNamespace(
            id=7,
            active=0,
            status="ACTIVE",
        )
        self.db.query.return_value.filter.return_value.first.return_value = user

        with patch.object(
            dependencies, "verify_token", return_value={"sub": "7"}
        ):
            with self.assertRaises(HTTPException) as context:
                dependencies.get_current_user(
                    credentials=self.credentials,
                    db=self.db,
                )

        self.assertEqual(context.exception.status_code, 403)

    def test_database_errors_are_not_converted_to_401(self):
        self.db.query.side_effect = RuntimeError("database unavailable")

        with patch.object(
            dependencies, "verify_token", return_value={"sub": "7"}
        ):
            with self.assertRaisesRegex(
                RuntimeError, "database unavailable"
            ):
                dependencies.get_current_user(
                    credentials=self.credentials,
                    db=self.db,
                )


if __name__ == "__main__":
    unittest.main()
