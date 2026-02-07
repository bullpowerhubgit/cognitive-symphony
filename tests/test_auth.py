"""
Tests für das Authentifizierungsmodul
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cognitive_symphony.auth.models import UserCreate, UserRole
from cognitive_symphony.auth.service import AuthService
from cognitive_symphony.auth.router import router
from cognitive_symphony.auth.dependencies import get_auth_service


@pytest.fixture
def auth_service():
    """Erstellt eine frische AuthService-Instanz für jeden Test"""
    return AuthService()


@pytest.fixture
def app(auth_service):
    """Erstellt eine FastAPI-App mit Auth-Router für Tests"""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_auth_service] = lambda: auth_service
    return app


@pytest.fixture
def client(app):
    """HTTP-Testclient"""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Beispiel-Benutzerdaten"""
    return UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="securepassword123",
    )


@pytest.fixture
def registered_user(auth_service, sample_user_data):
    """Registriert einen Benutzer und gibt ihn zurück"""
    return auth_service.register_user(sample_user_data)


# --- AuthService Unit Tests ---


class TestAuthServicePasswordHashing:
    """Tests für Passwort-Hashing"""

    def test_hash_password_returns_hash(self, auth_service):
        hashed = auth_service.hash_password("testpassword")
        assert hashed != "testpassword"
        assert len(hashed) > 0

    def test_verify_correct_password(self, auth_service):
        hashed = auth_service.hash_password("testpassword")
        assert auth_service.verify_password("testpassword", hashed) is True

    def test_verify_wrong_password(self, auth_service):
        hashed = auth_service.hash_password("testpassword")
        assert auth_service.verify_password("wrongpassword", hashed) is False


class TestAuthServiceTokens:
    """Tests für JWT-Token-Erstellung und -Validierung"""

    def test_create_access_token(self, auth_service):
        token = auth_service.create_access_token(
            data={"sub": "testuser", "role": "user"}
        )
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self, auth_service):
        token = auth_service.create_access_token(
            data={"sub": "testuser", "role": "user"}
        )
        token_data = auth_service.decode_token(token)
        assert token_data is not None
        assert token_data.username == "testuser"
        assert token_data.role == UserRole.USER

    def test_decode_invalid_token(self, auth_service):
        token_data = auth_service.decode_token("invalid.token.here")
        assert token_data is None


class TestAuthServiceRegistration:
    """Tests für Benutzerregistrierung"""

    def test_register_user_success(self, auth_service, sample_user_data):
        user = auth_service.register_user(sample_user_data)
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True

    def test_register_duplicate_username(self, auth_service, sample_user_data):
        auth_service.register_user(sample_user_data)
        duplicate = auth_service.register_user(sample_user_data)
        assert duplicate is None

    def test_register_duplicate_email(self, auth_service, sample_user_data):
        auth_service.register_user(sample_user_data)
        other_user = UserCreate(
            username="otheruser",
            email="test@example.com",
            password="anotherpassword123",
        )
        result = auth_service.register_user(other_user)
        assert result is None


class TestAuthServiceAuthentication:
    """Tests für Benutzer-Authentifizierung"""

    def test_authenticate_valid_credentials(self, auth_service, sample_user_data):
        auth_service.register_user(sample_user_data)
        token = auth_service.authenticate_user("testuser", "securepassword123")
        assert token is not None
        assert token.access_token
        assert token.token_type == "bearer"

    def test_authenticate_wrong_password(self, auth_service, sample_user_data):
        auth_service.register_user(sample_user_data)
        token = auth_service.authenticate_user("testuser", "wrongpassword")
        assert token is None

    def test_authenticate_nonexistent_user(self, auth_service):
        token = auth_service.authenticate_user("nobody", "password")
        assert token is None

    def test_authenticate_inactive_user(self, auth_service, sample_user_data):
        auth_service.register_user(sample_user_data)
        auth_service.deactivate_user("testuser")
        token = auth_service.authenticate_user("testuser", "securepassword123")
        assert token is None


class TestAuthServiceUserManagement:
    """Tests für Benutzerverwaltung"""

    def test_get_user(self, auth_service, registered_user):
        user = auth_service.get_user("testuser")
        assert user is not None
        assert user.username == "testuser"

    def test_get_nonexistent_user(self, auth_service):
        user = auth_service.get_user("nobody")
        assert user is None

    def test_deactivate_user(self, auth_service, registered_user):
        result = auth_service.deactivate_user("testuser")
        assert result is True
        user = auth_service.get_user("testuser")
        assert user.is_active is False

    def test_deactivate_nonexistent_user(self, auth_service):
        result = auth_service.deactivate_user("nobody")
        assert result is False


# --- API Endpoint Integration Tests ---


class TestRegisterEndpoint:
    """Tests für den Registrierungs-Endpoint"""

    def test_register_success(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "full_name": "New User",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "dupuser",
                "email": "dup@example.com",
                "password": "securepassword123",
            },
        )
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "dupuser",
                "email": "dup2@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 409

    def test_register_short_password(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "user",
                "email": "e@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestLoginEndpoint:
    """Tests für den Login-Endpoint"""

    def test_login_success(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "securepassword123",
            },
        )
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "loginuser", "password": "securepassword123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nobody", "password": "wrongpass"},
        )
        assert response.status_code == 401


class TestMeEndpoint:
    """Tests für den /me-Endpoint"""

    def test_get_me_authenticated(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "meuser",
                "email": "me@example.com",
                "password": "securepassword123",
            },
        )
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "meuser", "password": "securepassword123"},
        )
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "meuser"

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client):
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401


class TestDeactivateEndpoint:
    """Tests für den Deaktivierungs-Endpoint"""

    def _create_admin_token(self, client, auth_service):
        """Hilfsfunktion: Admin-Benutzer erstellen und Token holen"""
        admin_data = UserCreate(
            username="admin",
            email="admin@example.com",
            password="adminpassword123",
            role=UserRole.ADMIN,
        )
        auth_service.register_user(admin_data)
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "admin", "password": "adminpassword123"},
        )
        return login_response.json()["access_token"]

    def test_deactivate_as_admin(self, client, auth_service):
        admin_token = self._create_admin_token(client, auth_service)

        client.post(
            "/api/v1/auth/register",
            json={
                "username": "targetuser",
                "email": "target@example.com",
                "password": "securepassword123",
            },
        )

        response = client.post(
            "/api/v1/auth/deactivate/targetuser",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    def test_deactivate_as_non_admin(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "regularuser",
                "email": "regular@example.com",
                "password": "securepassword123",
            },
        )
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "regularuser", "password": "securepassword123"},
        )
        token = login_response.json()["access_token"]

        response = client.post(
            "/api/v1/auth/deactivate/someone",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_admin_cannot_deactivate_self(self, client, auth_service):
        admin_token = self._create_admin_token(client, auth_service)

        response = client.post(
            "/api/v1/auth/deactivate/admin",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400
