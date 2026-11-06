import unittest
from decimal import Decimal

from platform_core.universal_value.core.value_engine import (
    UniversalValueEngine,
)


class UniversalValueEngineUnitTests(unittest.TestCase):

    def setUp(self):
        self.engine = UniversalValueEngine()

    def calculate(self, currency=None):
        arguments = {
            "user_id": "USER-1",
            "event_id": "ENGINE-TEST-001",
            "source": "TEST",
            "base_value": Decimal("10"),
        }
        if currency is not None:
            arguments["currency"] = currency

        return self.engine.calculate(**arguments)

    def test_default_output_currency_is_point(self):
        result = self.calculate()
        self.assertEqual(result.currency, "POINT")

    def test_legacy_xp_output_currency_is_point(self):
        result = self.calculate(currency="XP")
        self.assertEqual(result.currency, "POINT")

    def test_economic_currency_is_preserved(self):
        result = self.calculate(currency="Drika")
        self.assertEqual(result.currency, "Drika")


if __name__ == "__main__":
    unittest.main()
