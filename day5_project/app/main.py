import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.auth.views  import router as auth_router
from src.users.views import router as users_router
from src.items.views import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Day 5 API started — OAuth2 + JWT")
    yield
    print("Day 5 API shutting down")


app = FastAPI(
    title="Day 5 — OAuth2 with JWT",
    version="5.0.0",
    lifespan=lifespan,
    description="""
                """,
    # Enables the Authorize button in Swagger UI
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,  prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(items_router, prefix="/api/v1")


@app.get("/", tags=["Info"])
async def root():
    return {
        "project": "Day 5 — OAuth2 with JWT",
        "docs":    "http://localhost:8004/docs",
        "steps": [
            "1. POST /api/v1/auth/signup",
            "2. POST /api/v1/auth/login  → get token",
            "3. Click Authorize in Swagger → paste token",
            "4. Access protected routes",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)
