from fastapi import status, FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


class DomainError(Exception):
    """Базовая доменная ошибка.

    Наследники задают status_code и (опционально) default_message.
    Обработчик ниже маппит любую DomainError в JSON-ответ.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_message: str = "bad request"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class AuthenticationError(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "unauthorized"

    headers: dict[str, str] = {"WWW-Authenticate": "Bearer"}


class PermissionDeniedError(DomainError):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "forbidden"


class NotFoundError(DomainError):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "not found"

class ConflictError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_message = "conflict"


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует глобальные обработчики ошибок в приложении FastAPI."""

    @app.exception_handler(DomainError)
    async def _domain_error_handler(
            request: Request, exc: DomainError
    ) -> JSONResponse:
        headers = getattr(exc, "headers", None)

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
            headers=headers,
        )