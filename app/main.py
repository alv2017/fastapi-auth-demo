from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session

from app.auth import router as auth_router
from app.db.connection import get_engine, get_session
from app.db.schema import Base
from app.db.schema import User as db_User
from app.logging import client_logger
from app.settings import oauth2_scheme, settings
from app.user_administration import router as user_admin_router
from app.users import router as user_router
from app.users.permissions import (
    authenticated_admin_user,
    authenticated_staff_user,
    authenticated_user,
)

ENABLE_CLIENT_LOGGING = settings.ENABLE_CLIENT_LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(title="User Authentication Demo", lifespan=lifespan)


if ENABLE_CLIENT_LOGGING:

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        response = await call_next(request)
        client_logger.info(
            "method: %s, call: %s, ip: %s, status: %s",
            request.method,
            request.url.path,
            request.client.host,
            response.status_code,
        )
        return response


@app.get("/")
def welcome():
    return {"api": "User Authentication Demo", "version": "v1"}


@app.get("/financial-markets/")
def get_financial_news(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_user),
):
    return {
        "title": "The Latest News from the Financial Markets",
        "description": "Financial news can be accessed by members only.",
        "message": f"Hi, {auth_user.username}!",
    }


@app.get("/company-insights/")
def get_staff_updates(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_staff_user),
):
    return {
        "title": "Company Insights",
        "description": "Company Insights can be accessed only by members of staff",
        "message": f"Hi, {auth_user.username}! Stay up to date with the latest Company events!",
    }


@app.get("/system-administration/")
def access_system_administration_resources(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_user: db_User = Depends(authenticated_admin_user),
):
    return {
        "title": "System Administration",
        "description": "System Administration resources can be accessed only by administrators only",
        "message": f"Hi, {auth_user.username}! Welcome to System Administration.",
    }


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(user_admin_router.router)
