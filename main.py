from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from typing import List
app = FastAPI()

openai.api_key = "MYKEY"

class RecipeRequest(BaseModel):
    ingredients: List[str]
    meal_type: str

class Recipe(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    instructions: str

recipes_db = []

async def get_recommendations(ingredients: List[str], meal_type: str):
    prompt = f"Suggest recipes using the following ingredients: {', '.join(ingredients)} for a {meal_type} meal."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    
      temperature = 0.7
    )
  
       recommendations = response['choices'][0]['message']['content']
    return recommendations

@app.get("/")
async def read_root():
    return {"message": "Welcome to Savorly!"}


@app.post("/recommend")
async def recommend(recipe_request: RecipeRequest):
    try:
        ingredients = recipe_request.ingredients
        meal_type = recipe_request.meal_type

        recommendations = await get_recommendations(ingredients, meal_type)
        
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recipes", response_model=List[Recipe])
async def get_all_recipes():
    return recipes_db

@app.post("/recipes", response_model=Recipe)
async def add_recipe(recipe: Recipe):
    if any(r.id == recipe.id for r in recipes_db):
        raise HTTPException(status_code=400, detail="Recipe ID already exists.")
    
    recipes_db.append(recipe)
    return recipe

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    for recipe in recipes_db:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found.")

