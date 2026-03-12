
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.items    import views as items_view
from src.products import views as products_view
from src.users    import views as users_view


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Day 4 API started — connected to PostgreSQL")
    yield
    print("🔒 Day 4 API shutting down")


app = FastAPI(
    title="Day 4 — SQLAlchemy (async) + PostgreSQL",
    version="4.0.0",
    lifespan=lifespan,
    description="""

## Quick Setup
```
1. createdb day4_db
2. alembic upgrade head
3. uvicorn app.main:app --reload --port 8003
```
""",
)

app.include_router(items_view.router,    prefix="/api/v1")
app.include_router(products_view.router, prefix="/api/v1")
app.include_router(users_view.router,    prefix="/api/v1")


@app.get("/", tags=["Info"])
async def root():
    return {
        "project": "Day 4 — SQLAlchemy (async) + PostgreSQL",
        "docs":    "http://localhost:8003/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)
