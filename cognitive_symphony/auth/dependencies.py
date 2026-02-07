"""
FastAPI-Abhängigkeiten für Authentifizierung
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from cognitive_symphony.auth.models import User, UserRole
from cognitive_symphony.auth.service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Globale AuthService-Instanz
_auth_service: AuthService | None = None


def get_auth_service() -> AuthService:
    """Gibt die AuthService-Instanz zurück"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Extrahiert den aktuellen Benutzer aus dem JWT-Token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Authentifizierungsdaten",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = auth_service.decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    user = auth_service.get_user(token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Stellt sicher, dass der Benutzer aktiv ist"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Benutzer ist deaktiviert",
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Stellt sicher, dass der Benutzer ein Administrator ist"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administratorrechte erforderlich",
        )
    return current_user
