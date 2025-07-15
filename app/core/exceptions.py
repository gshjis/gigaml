class TaskNotFoundError(Exception):
    """Вызывается когда задача не найдена"""

    pass

class UserAlreadyExistsError(Exception):
    """Raised when a user with the provided email already exists."""



class InvalidTaskDataError(Exception):
    """Вызывается при невалидных данных задачи"""

    pass


class TaskAlreadyExistsError(Exception):
    """Вызывается при попытке создать дубликат задачи"""

    pass


class DatabaseError(Exception):
    """Вызывается при ошибках работы с базой данных"""

    pass
