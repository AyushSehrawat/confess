import os
from datetime import timedelta
from typing import Optional, Any
from pathlib import Path

from dotenv import load_dotenv
import uvicorn
import asyncio

# FastAPI imports
from fastapi import FastAPI, HTTPException, Depends, Request, Form, Cookie, Response, Query
from fastapi.responses import RedirectResponse, JSONResponse, ORJSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

# Auth Library Imports
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException

# Pydantic & Deta imports
from pydantic import BaseModel

# Import the routers [ from src.view import main as view_main]
from src.confess import main as confess_main
from src.operations import post as operations_post

# Some Env Variables And Configurations
load_dotenv()
from src.database import user, posts
from src.models import UserModel

app = FastAPI(
    title="Confessioner",
    description="Share your confessions with the world while being anonymous",
    version="0.0.1",
    terms_of_service="/soon",
    contact={
        "name": "AyushSehrawat",
        "email": "mini@minidev.me",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url=None
)

# Jinja2 Templating
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "src/templates"))
app.mount("/assets", StaticFiles(directory=str(BASE_PATH / "src/assets")), name="assets")

class Settings(BaseModel):
    authjwt_secret_key: str = str(os.getenv("SECRET_KEY"))
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    access_expires: int = timedelta(days=7)
    # In case of error do authjwt_cookie_csrf_protect: bool = False

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    # If user not logged in redirect to /
    return RedirectResponse(url="/", status_code=303)

@app.get("/", include_in_schema=False)
async def index(request : Request):
    return TEMPLATES.TemplateResponse("index.html", {"request": request})

# Add the views like -> app.include_router(view_main.router)
app.include_router(confess_main.router)
app.include_router(operations_post.router)

if __name__ == '__main__':
    uvicorn.run("main:app",host='0.0.0.0', port=int(os.getenv("PORT")), reload=True, debug=True, workers=2)