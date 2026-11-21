import datetime
import logging
import jwt

from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Возвращает хэш пароля (bcrypt)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли пароль с хэшем."""
    return pwd_context.verify(plain_password, hashed_password)

class TokenError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class TokenTypeError(TokenError):
    def __init__(self, message: str = f"Ошибка типа токена"):
        super().__init__(message)

class TokenExpiredError(TokenError):
    def __init__(self, message: str = f"Токен просрочен"):
        super().__init__(message)

class TokenInvalidError(TokenError):
    def __init__(self, message: str = f"Токен невалидный"):
        super().__init__(message)

access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM

logger = logging.getLogger(__name__)

def create_jwt_token(user_id: str) -> str:
    expires_in = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=access_token_expire)

    data = {
        'sub': user_id,
        'exp': expires_in
    }
    token = jwt.encode(
        data,
        secret_key,
        algorithm=algorithm
    )
    logger.debug(f"JWT token created for session {user_id}")
    return token

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except jwt.InvalidTokenError:
        raise TokenInvalidError("Invalid token")