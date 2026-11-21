import pytest
import jwt
import datetime
from app.core.security import (
    hash_password,
    verify_password,
    create_jwt_token,
    verify_jwt_token,
    TokenExpiredError,
    TokenInvalidError
)
from app.core.config import settings


def test_password_hashing():
    """Проверяем, что хэш создается и не равен исходному паролю."""
    password = "super_secret_password"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$2b$")  # bcrypt хэши начинаются с этого префикса
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_verify_password_invalid_hash_format():
    """Проверяем, что битый хэш не роняет приложение, а возвращает False."""
    assert verify_password("any_password", "not_a_valid_bcrypt_hash") is False


def test_create_and_verify_jwt():
    """Проверяем, что токен создается и успешно расшифровывается."""
    user_id = 42
    token = create_jwt_token(user_id)

    assert isinstance(token, str)

    payload = verify_jwt_token(token)
    assert payload["sub"] == str(user_id)
    assert "exp" in payload


def test_verify_jwt_invalid_token():
    """Проверяем, что поддельный токен вызывает TokenInvalidError."""
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake_payload.fake_signature"
    with pytest.raises(TokenInvalidError):
        verify_jwt_token(fake_token)


def test_verify_jwt_expired_token():
    """Проверяем, что просроченный токен вызывает TokenExpiredError."""
    # Вручную создаем токен, который истек вчера
    expired_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    expired_token = jwt.encode(
        {"sub": "1", "exp": expired_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    with pytest.raises(TokenExpiredError):
        verify_jwt_token(expired_token)