import uuid
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=120)
    account_type: Literal["parent", "therapist"] = "parent"

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.lower()


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: str | None
    account_type: Literal["parent", "therapist"]


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut