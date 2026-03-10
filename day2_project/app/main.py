from fastapi import FastAPI
from app.routes.products import router

app = FastAPI(title="FastAPI Training — Day 2 Pydantic")

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "FastAPI Day 2 project is running",
        "docs": "http://localhost:8001/docs",
        "endpoints": "http://localhost:8001/products",
    }
