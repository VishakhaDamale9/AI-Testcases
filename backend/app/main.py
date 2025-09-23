import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.responses import FileResponse

from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins if settings.all_cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Total-Count"],
)

# Add a root route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI", "docs": "/docs", "api": "/api/v1"}

# favicon route
@app.get("/favicon.ico")
def read_favicon():
    return FileResponse("app/static/favicon.ico")

app.include_router(api_router, prefix=settings.API_V1_STR)
