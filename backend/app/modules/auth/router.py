from fastapi import APIRouter, status
from app.core.dependencies import DbSession, CurrentUser
from app.modules.auth import service
from app.modules.auth.schemas import LoginRequest, ChangePasswordRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DbSession) -> TokenResponse:
    result = await service.login(data.login, data.password, db)
    return TokenResponse(
        access_token=result['token'],
        expires_in=result['expire_time']
    )

@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(data: ChangePasswordRequest, current_user: CurrentUser, db: DbSession) -> None:
    await service.change_password(
        current_user, data.current_password, data.new_password, db
    )
