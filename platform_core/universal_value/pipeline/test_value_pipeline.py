import unittest
from decimal import Decimal

from platform_core.universal_value.core.value_request import ValueRequest
from platform_core.universal_value.pipeline.value_pipeline import ValuePipeline


class ValuePipelineUnitTests(unittest.TestCase):

    def setUp(self):
        self.pipeline = ValuePipeline()

    def make_request(self, currency="POINT"):
        return ValueRequest(
            user_id="USER-1",
            event_id="PIPELINE-TEST-001",
            source="TEST",
            action="test_action",
            base_value=Decimal("10"),
            currency=currency,
        )

    def test_default_point_currency_is_preserved(self):
        result = self.pipeline.calculate(self.make_request())
        self.assertEqual(result.currency, "POINT")

    def test_legacy_xp_currency_becomes_point(self):
        result = self.pipeline.calculate(
            self.make_request(currency="XP")
        )
        self.assertEqual(result.currency, "POINT")

    def test_economic_currency_is_preserved(self):
        result = self.pipeline.calculate(
            self.make_request(currency="Drika")
        )
        self.assertEqual(result.currency, "Drika")


if __name__ == "__main__":
    unittest.main()
