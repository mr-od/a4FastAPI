from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from core.config import get_settings


def include_router(app):
    app.include_router(api_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=get_settings().project_name,
                  version=get_settings().project_version)
    include_router(app)
    configure_static(app)
    return app


app = start_application()