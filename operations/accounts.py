import sys
import os
import json
from typing import Optional
import asyncio

from pydantic import BaseModel
from fastapi_another_jwt_auth import AuthJWT

from pathlib import Path

from dotenv import load_dotenv
import uvicorn
import asyncio

# FastAPI imports
from fastapi import APIRouter, HTTPException, Depends, Request, Response, Header
from fastapi import Request, Form
from fastapi import Response
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi import Form, Cookie, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

router = APIRouter(
    responses={404: {"description": "Not found"}}
)

# Jinja2 Templating
TEMPLATES = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/login", include_in_schema=False)
async def login(request : Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    if current_user == "anonymous":
        return TEMPLATES.TemplateResponse("login.html", {"request": request, "user": current_user})
    elif current_user != "anonymous":
        return RedirectResponse(url="/")

@router.get("/register", include_in_schema=False)
async def register(request : Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject() or "anonymous"
    if current_user == "anonymous":
        return TEMPLATES.TemplateResponse("register.html", {"request": request, "user": current_user})
    elif current_user != "anonymous":
        return RedirectResponse(url="/")