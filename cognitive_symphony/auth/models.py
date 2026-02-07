"""
Benutzer- und Authentifizierungsmodelle
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4


class UserRole(str, Enum):
    """Benutzerrollen im System"""

    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class UserBase(BaseModel):
    """Basis-Benutzermodell"""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=255)
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    """Modell für Benutzerregistrierung"""

    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Modell für Benutzer-Login"""

    username: str
    password: str


class User(UserBase):
    """Vollständiges Benutzermodell"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None


class UserInDB(User):
    """Benutzermodell mit gehashtem Passwort (nur intern)"""

    hashed_password: str


class Token(BaseModel):
    """JWT-Token-Antwort"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Dekodierte Token-Daten"""

    username: Optional[str] = None
    role: Optional[UserRole] = None
