import uuid
from datetime import datetime, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import decode_access_token
from db.models import TherapistProfile, User
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def account_type_of(db: Session, user: User) -> str:
    return "therapist" if db.get(TherapistProfile, user.id) else "parent"


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise _unauthorized
    user = db.get(User, user_id)
    if user is None or user.deleted_at is not None:
        raise _unauthorized
    return user


def require_therapist(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> User:
    if account_type_of(db, user) != "therapist":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Therapist account required")
    return user