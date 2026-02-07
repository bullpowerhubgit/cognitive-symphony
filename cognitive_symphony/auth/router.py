"""
API-Routen für Authentifizierung
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from cognitive_symphony.auth.dependencies import (
    get_auth_service,
    get_current_active_user,
    require_admin,
)
from cognitive_symphony.auth.models import Token, User, UserCreate
from cognitive_symphony.auth.service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Registriert einen neuen Benutzer"""
    user = auth_service.register_user(user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Benutzername oder E-Mail bereits vergeben",
        )
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authentifiziert einen Benutzer und gibt ein JWT-Token zurück"""
    token = auth_service.authenticate_user(form_data.username, form_data.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger Benutzername oder Passwort",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Gibt die Informationen des aktuellen Benutzers zurück"""
    return current_user


@router.post("/deactivate/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    username: str,
    admin_user: User = Depends(require_admin),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Deaktiviert einen Benutzer (nur Administratoren)"""
    if username == admin_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Eigenen Account kann nicht deaktiviert werden",
        )

    success = auth_service.deactivate_user(username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden",
        )
