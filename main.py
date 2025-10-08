import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.application.api import error_handlers, routers
from app.settings import settings
from app.utils import exceptions


def _include_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def _include_router(app: FastAPI) -> None:
    app.include_router(routers)


def _include_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exceptions.ObjectAlreadyExists,
        error_handlers.handle_object_already_exists # type: ignore
    )
    app.add_exception_handler(
        exceptions.ObjectNotFound,
        error_handlers.handle_object_not_found # type: ignore
    )
    app.add_exception_handler(
        exceptions.InvalidCredentials,
        error_handlers.handle_invalid_credentials # type: ignore
    )
    app.add_exception_handler(
        exceptions.UnauthorizedAction,
        error_handlers.handle_unauthorized_action # type: ignore
    )
    app.add_exception_handler(
        exceptions.PermissionDenied,
        error_handlers.handle_permission_denied # type: ignore
    )
    app.add_exception_handler(
        exceptions.FileTooLargeError,
        error_handlers.add_exception_handlers # type: ignore
    )
    app.add_exception_handler(
        exceptions.FileExtensionNotAllowedError,
        error_handlers.file_extension_not_allowed_handler # type: ignore
    )


def _mount_static_files(app: FastAPI) -> None:
    media_path = str(settings.file_storage.base_path)
    os.makedirs(media_path, exist_ok=True)
    app.mount("/media", StaticFiles(directory=media_path), name="media")


def create_app() -> FastAPI:
    app = FastAPI()
    _include_middleware(app)
    _include_router(app)
    _include_error_handlers(app)
    _mount_static_files(app)

    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", host=settings.HOST, port=settings.PORT)
