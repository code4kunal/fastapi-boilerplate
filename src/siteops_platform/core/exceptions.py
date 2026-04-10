"""Application and domain errors (map to HTTP in handlers)."""

from __future__ import annotations


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__("not_found", message, status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__("conflict", message, status_code=409)


class ValidationAppError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__("validation_error", message, status_code=422)