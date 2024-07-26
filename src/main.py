from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from sqladmin import Admin

from fastapi.middleware.cors import CORSMiddleware
from admin.auth_backend import AdminAuth
from advertisement.admin import AdvertisementAdmin
from user.admin import UserAdmin

from db import engine
from logger import app_logger as logger
from config import settings

from auth.router import router as auth_router
from auth.base_config import verify_user
from fixtures.loader import load_advertisement_fixture
from advertisement.router import router as advertisement_router


async def init_admin():
    """Initialize the admin interface with authentication and views."""
    admin_settings = settings.admin
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=AdminAuth(secret_key=admin_settings.ADMIN_SECRET_SESSION),
    )
    # Register admin views for managing advertisements and users
    admin_views = [AdvertisementAdmin, UserAdmin]
    [admin.add_view(view) for view in admin_views]


async def start_up(app: FastAPI):
    """Perform startup procedures when the application starts."""
    logger.debug("App started")
    # Load initial data for advertisements from the CSV file
    await load_advertisement_fixture(file_path=settings.fixtures.FIXTURES_PATH / "data" / "advertisements.csv")
    await init_admin()


async def shut_down(app: FastAPI):
    """Clean up resources on application shutdown."""
    logger.debug("Shutting down")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application lifespan with startup and shutdown processes."""
    await start_up(app)  # Perform startup tasks
    yield
    await shut_down(app)  # Perform shutdown tasks


app = FastAPI(lifespan=lifespan)


# Middleware settings to handle CORS (Cross-Origin Resource Sharing)
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


# Include routers for advertisements and authentication
app.include_router(
    advertisement_router,
    tags=["Advertisement"],
    prefix=f"/api/v{settings.api.API_VERSION}/advertisement",
    dependencies=[Depends(verify_user)]
)
app.include_router(
    auth_router, 
    tags=["Auth"], 
    prefix="/auth"
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)  # Start the application server