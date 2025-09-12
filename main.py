import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.application.api import error_handlers
from app.application.api import routers
from app.settings import settings
from app.utils import exceptions


def _include_router(app: FastAPI) -> None:
    app.include_router(routers)


def _include_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(exceptions.ObjectAlreadyExists, error_handlers.handle_object_already_exists)
    app.add_exception_handler(exceptions.ObjectNotFound, error_handlers.handle_object_not_found)
    app.add_exception_handler(exceptions.InvalidCredentials, error_handlers.handle_invalid_credentials)
    app.add_exception_handler(exceptions.UnauthorizedAction, error_handlers.handle_unauthorized_action)
    app.add_exception_handler(exceptions.PermissionDenied, error_handlers.handle_permission_denied)
    app.add_exception_handler(exceptions.FileTooLargeError, error_handlers.add_exception_handlers)
    app.add_exception_handler(exceptions.FileExtensionNotAllowedError, error_handlers.file_extension_not_allowed_handler)

def _mount_static_files(app: FastAPI) -> None:
    app.mount("/media", StaticFiles(directory=str(settings.file_storage.base_path)), name="media")

def create_app() -> FastAPI:
    app = FastAPI()
    _include_router(app)
    _include_error_handlers(app)
    _mount_static_files(app)

    return app


if __name__ == "__main__":
    # subprocess.Popen([
    #     sys.executable, "-m", "celery",
    #     "-A", "app.infrastructure.celery.celery_app.celery_app",
    #     "worker", "--loglevel=info", "--pool=solo"
    # ])
    # subprocess.Popen([
    #     sys.executable, "-m", "celery",
    #     "-A", "app.infrastructure.celery.celery_app.celery_app",
    #     "beat", "--loglevel=info"
    # ])
    uvicorn.run("main:create_app", host=settings.HOST, port=settings.PORT)
