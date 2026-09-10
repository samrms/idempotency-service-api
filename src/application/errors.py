class AppError(Exception):
    """Base class for expected application errors."""


class ConflictError(AppError):
    """The idempotency key was reused with a different request."""


class NotFoundError(AppError):
    """The requested resource does not exist."""
