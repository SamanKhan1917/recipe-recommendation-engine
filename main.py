from fastapi import FastAPI
from . import routes

app = FastAPI()

app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe Recommendation System!"}
