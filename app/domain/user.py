from dataclasses import dataclass


@dataclass
class UserData:
    """Класс предназначен для передачи между всеми слоями кроме handlers."""

    user_id: int
    username: str
    email: str
    hashed_password: str
