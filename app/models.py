from pydantic import BaseModel, validator, Field, EmailStr
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Any

# Ignore code editor saying self needed under validator

class UserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = Field(...)
    is_staff: bool = Field(...)
    created_at: Optional[datetime]

    # Create validator for name,password,email fields to check if they are not empty and below 30 chars
    @validator('name', 'password', 'email')
    def check_empty_and_len(cls, v):
        if not v:
            raise ValueError("This field is required")
        if len(v) > 30:
            raise ValueError("This field is too long")
        return v

    # Create validator for is_admin,is_staff fields to check if they are boolean values
    @validator('is_admin', 'is_staff')
    def check_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("This field must be boolean")
        return v

    # Add created_at field to set the current time when user is created
    @validator('created_at', pre=True, always=True)
    def set_created_at(cls, v):
        return v or datetime.now()


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "secret",
                "is_admin": False,
                "is_staff": False,
                "created_at": "2020-01-01T00:00:00.000000Z"
            }
        }


# Example Usage
"""
lel = UserModel(name="Jane Doe", email="abc@gmail.com", password="secret", is_admin=False, is_staff=False)
print(jsonable_encoder(lel))
"""