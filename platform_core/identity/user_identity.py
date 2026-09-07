class UserIdentity:
    """
    Universal User Identity.

    This layer represents the ecosystem-wide identity of a user.
    Gateway identities such as Telegram are external links and
    must not become the primary user identity.
    """

    def __init__(self, internal_user_id: int):
        self.internal_user_id = internal_user_id
        self.user_id = None
        self.personal_code = None

    def set_user_id(self, user_id: str):
        from .user_id import validate_user_id, parse_user_id

        if not validate_user_id(user_id):
            raise ValueError("Invalid 17-digit user ID")

        self.user_id = str(user_id)
        self.personal_code = parse_user_id(user_id)["personal_code"]

    def is_finalized(self) -> bool:
        return self.user_id is not None

    def get_personal_code(self):
        return self.personal_code
