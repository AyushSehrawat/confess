from pydantic import BaseModel, validator, Field, EmailStr
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Optional, Any
from fastapi import FastAPI, Form
from fastapi.exceptions import HTTPException

import inspect
from typing import Type
import pydantic
from pydantic.fields import ModelField
# Ignore code editor saying self needed under validator


def validate_base_model(username, password, confirm_password):
    default = False
    if (len(username), len(password), len(confirm_password)) > (30,30,30):
        default = True # True cus they passed validation
    if password != confirm_password:
        default = True
    return default

def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    try:
        new_params = [
            inspect.Parameter(
                field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=(Form(field.default) if not field.required else Form(...)),
            )
            for field in cls.__fields__.values()
        ]

        async def _as_form(**data):
            return cls(**data)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig
        setattr(cls, "as_form", _as_form)
        return cls
    except pydantic.ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@as_form
class UserModel(BaseModel):
    username : str
    password : str
    confirm_password : str
    is_admin : Optional[bool] = False
    is_staff : Optional[bool] = False
    created_at : Optional[datetime] = datetime.now()

@as_form
class LoginModel(BaseModel):
    username : str
    password : str