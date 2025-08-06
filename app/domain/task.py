from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TaskData:
    task_id: int
    name: str
    pomodoro_count: int
    category_id: int
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime
