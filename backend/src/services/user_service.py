import jwt
from sqlalchemy.exc import IntegrityError

from src.core.security import decode_access_token, hash_password, verify_password
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate, UserLogin


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidAccessTokenError(Exception):
    pass


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def signup(self, data: UserCreate) -> User:
        email = data.email.lower()

        if self.repo.get_by_email(email) is not None:
            raise EmailAlreadyRegisteredError()

        user = User(
            full_name=data.full_name,
            email=email,
            password_hash=hash_password(data.password),
            date_of_birth=data.date_of_birth,
            nationality=data.nationality,
        )

        try:
            return self.repo.create(user)
        except IntegrityError:
            raise EmailAlreadyRegisteredError()

    def authenticate(self, data: UserLogin) -> User:
        email = data.email.lower()
        user = self.repo.get_by_email(email)

        if user is None or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        return user

    def get_current_user(self, token: str) -> User:
        try:
            payload = decode_access_token(token)
            user_id = int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            raise InvalidAccessTokenError() from None

        user = self.repo.get_by_id(user_id)
        if user is None:
            raise InvalidAccessTokenError()

        return user