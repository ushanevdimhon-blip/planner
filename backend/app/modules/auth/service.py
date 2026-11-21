import logging

from app.core.config import settings
from app.core.security import create_jwt_token, hash_password, verify_password
from app.modules.users.models import User
from app.core.exceptions import AuthenticationError, ConflictError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

async def login(login: str, password: str, db: AsyncSession) -> dict:
    user = await db.scalar(select(User).where(User.login == login))

    if user is None or not verify_password(password, user.hashed_password):
        logger.debug(f'login failed: {login}')
        raise AuthenticationError('Invalid credentials')

    token = create_jwt_token(user.id)
    expire_time = settings.ACCESS_TOKEN_EXP_MINUTES * 60

    logger.debug(f'login successful: {login}, user_id: {user.id}')
    return {'token': token, 'expire_time': expire_time}

async def change_password(user: User, password: str, new_password: str, db: AsyncSession):
    if not verify_password(password, user.hashed_password):
        logger.debug(f'change password failed for user_id: {user.id}')
        raise AuthenticationError('Invalid credentials')
    if password == new_password:
        raise ConflictError('new password must differ from current')

    user.hashed_password = hash_password(new_password)
    await db.commit()
    logger.debug(f'password changed for {user.id}')