from pydantic import BaseModel
from typing import List

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    instructions: str
    course_type: str

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True
