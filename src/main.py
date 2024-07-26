from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from advertisement.admin import AdvertisementAdmin
from admin.auth_backend import AdminAuth
from fastapi.middleware.cors import CORSMiddleware

from db import engine
from logger import app_logger as logger
from config import settings

from auth.router import router as auth_router
from advertisement.router import router as advertisement_router


async def init_admin():
    admin_settings = settings.admin
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=AdminAuth(secret_key=admin_settings.ADMIN_SECRET_SESSION),
    )
    admin_views = [AdvertisementAdmin]
    [admin.add_view(view) for view in admin_views]


async def start_up(app: FastAPI):
    logger.debug("App started")
    await init_admin()


async def shut_down(app: FastAPI):
    logger.debug("Shutting down")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_up(app)
    yield
    await shut_down(app)


app = FastAPI(lifespan=lifespan)


middleware_settings = settings.middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=middleware_settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


app.include_router(
    advertisement_router,
    tags=["Advertisement"],
    prefix=f"/api/v{settings.api.API_VERSION}/advertisement",
)


app.include_router(
    auth_router, 
    tags=["Auth"], 
    prefix="/auth"
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
