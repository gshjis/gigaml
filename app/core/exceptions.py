class TaskNotFoundError(Exception):
    """Вызывается когда задача не найдена"""

    pass


class InvalidTaskDataError(Exception):
    """Вызывается при невалидных данных задачи"""

    pass


class TaskAlreadyExistsError(Exception):
    """Вызывается при попытке создать дубликат задачи"""

    pass


class DatabaseError(Exception):
    """Вызывается при ошибках работы с базой данных"""

    pass
