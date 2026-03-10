from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="FastAPI Training CRUD (No Pydantic)")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "FastAPI training project is running"}