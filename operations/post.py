import sys
import os
import json
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Response, Header
from fastapi import Request, Form
from fastapi import Response
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    StreamingResponse,
)
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi_another_jwt_auth import AuthJWT
from utils.database import user, posts
from utils.models import validate_base_model, as_form, UserModel, LoginModel

router = APIRouter(prefix="/post", responses={404: {"description": "Not found"}})


@router.post("/register", include_in_schema=False)
async def post_register(
    request: Request,
    Authorize: AuthJWT = Depends(),
    form_data: UserModel = Depends(UserModel.as_form),
):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    result = validate_base_model(
        form_data.username, form_data.password, form_data.confirm_password
    )
    if result == False:
        if current_user == "anonymous":
            access_token = Authorize.create_access_token(subject=form_data.username)
            response = RedirectResponse(url="/", status_code=303)
            Authorize.set_access_cookies(access_token, response=response)
            # Convert form_data to dict and avoid datetime serialization error
            user_data = form_data.dict()
            user_data["created_at"] = str(user_data["created_at"])
            user.put(data=user_data, key=form_data.username)
            return response
        elif current_user != "anonymous":
            return RedirectResponse(url="/", status_code=303)
    elif result == True:
        return JSONResponse(content={"message": "Invalid form data"}, status_code=400)


@router.post("/login", include_in_schema=False)
async def post_login(
    request: Request,
    Authorize: AuthJWT = Depends(),
    form_data: LoginModel = Depends(LoginModel.as_form),
):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    if current_user == "anonymous":
        if (data := user.get(key=form_data.username)) is not None:
            if data["password"] == form_data.password:
                access_token = Authorize.create_access_token(subject=form_data.username)
                response = RedirectResponse(url="/", status_code=303)
                Authorize.set_access_cookies(access_token, response=response)
                return response
            else:
                return JSONResponse(
                    content={"message": "Invalid password"}, status_code=400
                )
        elif user.get(key=form_data.username) == None:
            return JSONResponse(
                content={"message": "Invalid credentials"}, status_code=400
            )
    elif current_user != "anonymous":
        return RedirectResponse(url="/", status_code=303)
