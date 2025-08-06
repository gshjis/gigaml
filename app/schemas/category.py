from pydantic import BaseModel


class CategorySchemaInput(BaseModel):
    name: str


class CategorySchemaOutput(BaseModel):
    category_id: int
    name: str
