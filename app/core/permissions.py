from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ALL = [READ, WRITE, DELETE]

# Register the Role enum with SQLAlchemy
RoleEnum = SQLAlchemyEnum(Role, name="role")