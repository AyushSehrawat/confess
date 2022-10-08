import os
from datetime import timedelta
from typing import Optional, Any
from pathlib import Path

# FastAPI imports
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request,
    Form,
    Cookie,
    Response,
    Query,
)
from fastapi.responses import (
    RedirectResponse,
    JSONResponse,
    ORJSONResponse,
    HTMLResponse,
    FileResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Auth Library Imports
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException

# Pydantic & Deta imports
from pydantic import BaseModel

# Import the routers [ from view import main as view_main]
from operations import accounts as confess_main
from operations import post as operations_post

# Some Env Variables And Configurations
from utils.database import user, posts
from utils.models import UserModel

app = FastAPI(
    title="Confess",
    description="Share your confessions with the world while being anonymous.",
    version="1",
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
    redoc_url=None,
)

# Jinja2 Templating
TEMPLATES = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Settings(BaseModel):
    authjwt_secret_key: str = str(os.environ["SECRET_KEY"])
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
async def index(request: Request):
    return TEMPLATES.TemplateResponse("index.html", {"request": request})


@app.get("/media/confess-logo", response_class=FileResponse)
async def confess_logo(request: Request):
    return "./media/confess.png"


# Add the views like -> app.include_router(view_main.router)
app.include_router(confess_main.router)
app.include_router(operations_post.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
