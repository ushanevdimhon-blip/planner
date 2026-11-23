from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_jwt_token, TokenExpiredError, TokenInvalidError
from app.core.db import get_db
from app.modules.users.models import User
from app.core.exceptions import AuthenticationError

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if credentials is None:
        raise AuthenticationError("Missing token")
    try:
        payload = verify_jwt_token(credentials.credentials)
    except TokenExpiredError:
        raise AuthenticationError("Token expired")
    except TokenInvalidError:
        raise AuthenticationError("Invalid token")

    user_id = payload["sub"]
    user = await db.get(User, int(user_id))
    if user is None:
        raise AuthenticationError("User not found")

    return user

DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]