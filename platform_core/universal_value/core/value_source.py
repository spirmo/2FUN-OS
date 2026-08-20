"""
2FUN Universal Value Infrastructure (UVI)
Universal Value Source Contract
"""

from enum import Enum


class ValueSource(str, Enum):
    """
    منابع رسمی ارزش در اکوسیستم 2FUN.

    این Enum قابل توسعه است و نباید منطق محاسباتی
    یک Source را در خود نگه دارد.
    """

    KNOWLEDGE = "KNOWLEDGE"
    GAME = "GAME"
    IDENTITY = "IDENTITY"
    ECONOMY = "ECONOMY"
    GOVERNANCE = "GOVERNANCE"
    REPUTATION = "REPUTATION"
    CONTRIBUTION = "CONTRIBUTION"
    CHALLENGE = "CHALLENGE"
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    WALLET = "WALLET"
    EXCHANGE = "EXCHANGE"
    METAVERSE = "METAVERSE"
    BLOCKCHAIN = "BLOCKCHAIN"
    SYSTEM = "SYSTEM"

    @classmethod
    def is_valid(cls, source: str) -> bool:
        return source in {item.value for item in cls}
