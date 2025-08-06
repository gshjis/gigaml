from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    """Исключение, выбрасываемое, когда пользователь с таким адресом электронной почты уже существует."""

    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )


class UserNotFoundException(HTTPException):
    """Исключение, выбрасываемое, когда пользователь не найден."""

    def __init__(self, message: str = "User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class InvalidCredentialsException(HTTPException):
    """Invalid credentials exception"""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )


class InvalidTokenException(HTTPException):
    """Invalid token exception"""

    def __init__(self, message: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )


class TaskNotFoundException(HTTPException):
    """Исключение, выбрасываемое, когда задача не найдена."""

    def __init__(self, message: str = "Task not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class DatabaseError(HTTPException):
    """Исключение, выбрасываемое при ошибке базы данных."""

    def __init__(self, message: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
