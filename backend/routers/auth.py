from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.deps import account_type_of, get_current_user, require_therapist
from core.security import create_access_token, hash_password, verify_password
from db.models import OrgMembership, Organisation, TherapistProfile, User
from db.session import get_db
from schemas.auth import RegisterRequest, TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_out(user: User, account_type: str) -> UserOut:
    return UserOut(id=user.id, email=user.email,
                   display_name=user.display_name, account_type=account_type)


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == body.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")

    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        preferred_language="en",
    )
    db.add(user)
    db.flush()  # assigns user.id

    if body.account_type == "therapist":
        db.add(TherapistProfile(
            user_id=user.id,
            primary_discipline_key="slt",
            verification_status="pending",
        ))
        org = Organisation(
            name=f"{body.display_name} (solo practice)",
            org_type="solo",
            solo_owner_user_id=user.id,
            country_code="PK",
            timezone="Asia/Karachi",
            directory_opt_in=False,
        )
        db.add(org)
        db.flush()
        db.add(OrgMembership(
            org_id=org.id,
            user_id=user.id,
            role="therapist",
            discipline_key="slt",
            status="active",
            started_at=datetime.now(timezone.utc),
        ))

    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, body.account_type)
    return TokenOut(access_token=token, user=_user_out(user, body.account_type))


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # the form field is called "username"; we use it for the email
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or user.deleted_at or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    account_type = account_type_of(db, user)
    token = create_access_token(user.id, account_type)
    return TokenOut(access_token=token, user=_user_out(user, account_type))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _user_out(user, account_type_of(db, user))


@router.get("/therapist-area")
def therapist_area(user: User = Depends(require_therapist)):
    """Temporary endpoint to prove role enforcement works."""
    return {"message": f"Welcome, therapist {user.display_name}"}