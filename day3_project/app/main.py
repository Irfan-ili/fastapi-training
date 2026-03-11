from fastapi import FastAPI

# ✅ FIX: import views module, access .router from it
from app.src.items    import views as items_view
from app.src.products import views as products_view
from app.src.users    import views as users_view

app = FastAPI(
    title="Day 3 — Depends() & Dependency Injection",
    version="3.0.0",
    description="""

## Auth Header (for DELETE endpoints)
```
X-Token: secret-day3-token
```
""",
)

app.include_router(items_view.router,    prefix="/api/v1")
app.include_router(products_view.router, prefix="/api/v1")
app.include_router(users_view.router,    prefix="/api/v1")


@app.get("/", tags=["Info"])
def root():
    return {
        "project": "Day 3 — Depends() & Dependency Injection",
        "docs":    "http://localhost:8002/docs",
        "routes": {
            "items":    "/api/v1/items/",
            "products": "/api/v1/products/",
            "users":    "/api/v1/users/",
            "config":   "/api/v1/users/config",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
