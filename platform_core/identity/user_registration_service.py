from sqlalchemy.orm import Session

from db.models.user import User
from .gateway_identity import GatewayIdentity
from .gateway_identity_repository import GatewayIdentityRepository
from .user_identity import UserIdentity
from .user_id_allocator import UserIdAllocator


class UserRegistrationService:
    """
    Account Registration Service.

    Each gateway credential resolves to one independent Account/User.

    Gateway identity is an external credential and is never used
    to merge multiple Accounts belonging to the same person.
    """

    def __init__(self, db_path="db/2fun.db"):
        self.allocator = UserIdAllocator(db_path)
        self.gateway_repository = GatewayIdentityRepository()

    def find_existing_user(
        self,
        session: Session,
        gateway: str,
        external_id: str,
    ):
        gateway_identity = GatewayIdentity(
            gateway,
            external_id,
        )

        row = self.gateway_repository.find_user(
            session,
            gateway_identity.gateway,
            gateway_identity.external_id,
        )

        if row is None:
            return None

        return session.get(User, row.id)

    def finalize_user_identity(
        self,
        session: Session,
        user: User,
        country,
        province,
        county,
        city,
    ):
        """
        Finalize the Account's 17-digit User ID.

        The ID is allocated exactly once for this Account.
        Allocation participates in the current SQLAlchemy transaction.
        """

        if user.user_id:
            return user

        if any(
            value is None
            for value in (
                country,
                province,
                county,
                city,
            )
        ):
            raise ValueError(
                "Complete geographic identity is required"
            )

        connection = session.connection().connection

        allocation = self.allocator.allocate(
            country,
            province,
            county,
            city,
            conn=connection,
        )

        identity = UserIdentity(user.id)
        identity.set_user_id(
            allocation["user_id"]
        )

        user.user_id = allocation["user_id"]

        session.flush()

        return user

    def register_user(
        self,
        session: Session,
        gateway: str,
        external_id: str,
        language=None,
        username=None,
        country=None,
        province=None,
        county=None,
        city=None,
    ):
        gateway_identity = GatewayIdentity(
            gateway,
            external_id,
        )

        existing = self.find_existing_user(
            session,
            gateway_identity.gateway,
            gateway_identity.external_id,
        )

        if existing:
            return existing

        user = User(
            language=language,
            username=username,
            status="ACTIVE",
            active=1,
        )

        # Preserve the existing Telegram compatibility field.
        if gateway_identity.gateway == "telegram":
            user.telegram_id = int(
                gateway_identity.external_id
            )

        session.add(user)
        session.flush()

        if all(
            value is not None
            for value in (
                country,
                province,
                county,
                city,
            )
        ):
            self.finalize_user_identity(
                session,
                user,
                country,
                province,
                county,
                city,
            )

        self.gateway_repository.link(
            session,
            user.id,
            gateway_identity.gateway,
            gateway_identity.external_id,
        )

        session.commit()
        session.refresh(user)

        return user
