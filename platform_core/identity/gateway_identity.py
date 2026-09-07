class GatewayIdentity:
    """
    External identity linked to the universal ecosystem User.

    A gateway identity (Telegram, Mobile, Web, etc.) is not
    the primary User identity.
    """

    def __init__(self, gateway: str, external_id: str):
        if not gateway:
            raise ValueError("Gateway is required")

        if not external_id:
            raise ValueError("External identity is required")

        self.gateway = gateway
        self.external_id = str(external_id)

    def key(self) -> tuple[str, str]:
        return self.gateway, self.external_id
