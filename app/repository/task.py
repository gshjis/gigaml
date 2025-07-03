from app.models import Task
from app.repository.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Репозиторий для работы с задачами."""

    @property
    def model(self) -> type[Task]:
        return Task
