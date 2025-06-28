from pydantic import BaseModel, Field, model_validator

class Task(BaseModel):
    id:int | None = None
    name:str | None = None
    pomodoro_count:int | None = None
    category_id:int

    @model_validator(mode = "after")
    def check_name_or_pomodoro_count_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Name or pomodoro_count must be provided.")
        return self
        
    