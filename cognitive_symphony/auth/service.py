"""
Authentifizierungs-Service mit JWT und Passwort-Hashing
"""

from datetime import datetime, timedelta
from typing import Dict, Optional

import bcrypt
import jwt
import structlog

from cognitive_symphony.auth.models import (
    Token,
    TokenData,
    User,
    UserCreate,
    UserInDB,
    UserRole,
)
from cognitive_symphony.config import settings

logger = structlog.get_logger()


class AuthService:
    """Service für Authentifizierung und Benutzerverwaltung"""

    def __init__(self):
        self._users_db: Dict[str, UserInDB] = {}
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm
        self._access_token_expire_minutes = settings.access_token_expire_minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Überprüft ein Passwort gegen den Hash"""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def hash_password(self, password: str) -> str:
        """Erstellt einen Passwort-Hash"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Erstellt ein JWT-Access-Token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=self._access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[TokenData]:
        """Dekodiert und validiert ein JWT-Token"""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            username: str = payload.get("sub")
            role: str = payload.get("role")
            if username is None:
                return None
            return TokenData(username=username, role=UserRole(role) if role else None)
        except (jwt.InvalidTokenError, Exception):
            return None

    def register_user(self, user_data: UserCreate) -> Optional[User]:
        """Registriert einen neuen Benutzer"""
        if user_data.username in self._users_db:
            logger.warning("registration_failed_duplicate", username=user_data.username)
            return None

        for existing_user in self._users_db.values():
            if existing_user.email == user_data.email:
                logger.warning("registration_failed_email_exists", email=user_data.email)
                return None

        hashed_password = self.hash_password(user_data.password)
        user_in_db = UserInDB(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            hashed_password=hashed_password,
        )

        self._users_db[user_data.username] = user_in_db

        logger.info("user_registered", username=user_data.username, role=user_data.role.value)

        return User(
            id=user_in_db.id,
            username=user_in_db.username,
            email=user_in_db.email,
            full_name=user_in_db.full_name,
            role=user_in_db.role,
            is_active=user_in_db.is_active,
            created_at=user_in_db.created_at,
        )

    def authenticate_user(self, username: str, password: str) -> Optional[Token]:
        """Authentifiziert einen Benutzer und gibt ein Token zurück"""
        user = self._users_db.get(username)
        if not user:
            logger.warning("auth_failed_user_not_found", username=username)
            return None

        if not self.verify_password(password, user.hashed_password):
            logger.warning("auth_failed_invalid_password", username=username)
            return None

        if not user.is_active:
            logger.warning("auth_failed_inactive_user", username=username)
            return None

        user.last_login = datetime.now()

        access_token = self.create_access_token(
            data={"sub": user.username, "role": user.role.value}
        )

        logger.info("user_authenticated", username=username)

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=self._access_token_expire_minutes * 60,
        )

    def get_user(self, username: str) -> Optional[User]:
        """Gibt einen Benutzer zurück (ohne Passwort)"""
        user_in_db = self._users_db.get(username)
        if user_in_db is None:
            return None

        return User(
            id=user_in_db.id,
            username=user_in_db.username,
            email=user_in_db.email,
            full_name=user_in_db.full_name,
            role=user_in_db.role,
            is_active=user_in_db.is_active,
            created_at=user_in_db.created_at,
            last_login=user_in_db.last_login,
        )

    def deactivate_user(self, username: str) -> bool:
        """Deaktiviert einen Benutzer"""
        user = self._users_db.get(username)
        if user is None:
            return False
        user.is_active = False
        logger.info("user_deactivated", username=username)
        return True
