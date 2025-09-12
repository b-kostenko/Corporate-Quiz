from typing import Any, Optional


class ObjectAlreadyExists(Exception):
    def __init__(self, message: Optional[str] = ""):
        super().__init__(message)


class ObjectNotFound(Exception):
    def __init__(self, model_name: str, id_: Any) -> None:
        self.msg = f"{model_name} with given identifier - {id_} not found"
        super().__init__(self.msg)


class InvalidCredentials(Exception):
    def __init__(self, message: Optional[str] = "Invalid credentials provided") -> None:
        super().__init__(message)

class UnauthorizedAction(Exception):
    def __init__(self, message: str = "You are not allowed to perform this action."):
        self.message = message
        super().__init__(self.message)

class PermissionDenied(Exception):
    def __init__(self, message: str = "You don't have permission to perform this action.") -> None:
        self.message = message
        super().__init__(self.message)

class FileTooLargeError(Exception):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.message = f"File size exceeds maximum allowed size of {self.max_size} bytes"
        super().__init__(self.message)


class FileExtensionNotAllowedError(Exception):
    def __init__(self, extension: str, allowed: list[str]):
        self.extension = extension
        self.allowed = allowed
        self.message = f"File extension '{self.extension}' is not allowed. Allowed extensions: {self.allowed}"
        super().__init__(self.message)