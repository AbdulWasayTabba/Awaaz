import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class InviteOut(BaseModel):
    code: str
    expires_at: datetime


class EnrollRequest(BaseModel):
    code: str = Field(min_length=6, max_length=16)


class EnrollmentOut(BaseModel):
    child_id: uuid.UUID
    organisation: str
    therapist: str | None