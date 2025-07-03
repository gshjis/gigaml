from app.models import Categorie
from app.repository.repository import BaseRepository


class CategoryRepository(BaseRepository[Categorie]):
    """Репозиторий для работы с задачами."""

    @property
    def model(self) -> type[Categorie]:
        return Categorie
