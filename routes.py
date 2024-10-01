from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal
import openai
import os
from dotenv import load_dotenv

load_dotenv()  


openai.api_key = os.getenv('OPENAI_API_KEY')

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recommendations/", response_model=List[schemas.Recipe])
async def get_recommendations(vegetables: str, spices: str, fats: str, course_type: str, db: Session = Depends(get_db)):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Recommend 6 recipes using these ingredients: {vegetables}, {spices}, {fats}, for {course_type}."}
        ]
    )
    recipes = response['choices'][0]['message']['content']
    return recipes
