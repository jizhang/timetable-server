from pydantic import BaseModel


class Category(BaseModel):
    id: int
    title: str
    color: str


class CategoryResponse(BaseModel):
    categories: list[Category]
