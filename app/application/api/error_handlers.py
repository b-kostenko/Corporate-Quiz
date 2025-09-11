from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.utils import exceptions as base_exc


def handle_object_not_found(_: Request, e: base_exc.ObjectNotFound) -> JSONResponse:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_404_NOT_FOUND)


def handle_object_already_exists(_: Request, e: base_exc.ObjectAlreadyExists) -> JSONResponse:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_409_CONFLICT)


def handle_invalid_credentials(_: Request, e: base_exc.InvalidCredentials) -> JSONResponse:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_401_UNAUTHORIZED)


def handle_unauthorized_action(_: Request, e: base_exc.UnauthorizedAction) -> JSONResponse:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_403_FORBIDDEN)


def handle_permission_denied(_: Request, e: base_exc.PermissionDenied) -> JSONResponse:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_403_FORBIDDEN)
