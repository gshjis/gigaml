from dataclasses import dataclass


@dataclass
class UserData:
    user_id: int
    username: str
    email: str
    hashed_password: str
