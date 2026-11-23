import pytest
from httpx import AsyncClient
from app.modules.users.models import User

# === ТЕСТЫ ЛОГИНА ===

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_non_existent_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "ghost", "password": "anypassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_validation_error(client: AsyncClient):
    """Проверяем, что Pydantic отсекает пустые поля (422 Unprocessable Entity)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "", "password": ""}  # min_length=1 упадет
    )
    assert response.status_code == 422


# === ТЕСТЫ СМЕНЫ ПАРОЛЯ ===

@pytest.mark.asyncio
async def test_change_password_unauthorized(client: AsyncClient):
    """Без токена менять пароль нельзя (401)."""
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"current_password": "old", "new_password": "newpassword123"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_change_password_success(client: AsyncClient, test_user: User):
    # 1. Логинимся, получаем токен
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "testpassword123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Меняем пароль
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"current_password": "testpassword123", "new_password": "newpassword456"},
        headers=headers
    )
    assert response.status_code == 204

    # 3. Проверяем, что старый пароль больше не работает
    old_login = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "testpassword123"}
    )
    assert old_login.status_code == 401

    # 4. Проверяем, что новый пароль работает
    new_login = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "newpassword456"}
    )
    assert new_login.status_code == 200

@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient, test_user: User):
    """Неверный текущий пароль не дает сменить на новый (401)."""
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "testpassword123"}
    )
    token = login_res.json()["access_token"]

    response = await client.post(
        "/api/v1/auth/change-password",
        json={"current_password": "wrong_current", "new_password": "newpassword456"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_change_password_same_as_old(client: AsyncClient, test_user: User):
    """Нельзя сменить пароль на точно такой же (409 Conflict)."""
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"login": "testuser", "password": "testpassword123"}
    )
    token = login_res.json()["access_token"]

    response = await client.post(
        "/api/v1/auth/change-password",
        json={"current_password": "testpassword123", "new_password": "testpassword123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "new password must differ from current"