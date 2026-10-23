from datetime import date
from typing import Literal
import uuid   
from pydantic import BaseModel, Field, field_validator

class Child_Create(BaseModel):
    name : str =  Field(min_length = 2, max_length = 40)
    dob : date
    sex : Literal["male", "female"]
    @field_validator("dob")
    @classmethod
    def dob_not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("date of birth cannot be in the future")
        return v

class Child_Out(BaseModel):
    id : uuid.UUID
    name : str
    dob : date
    age_in_months : int
    is_linked: bool = False