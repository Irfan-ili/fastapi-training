from fastapi import APIRouter, Depends, HTTPException

from app.database.fake_db  import FakeDatabase
from app.dependencies.db   import get_db
from app.dependencies.pagination import PaginationParams, get_pagination, paginate_list
from app.core.config       import Settings, get_settings
from app.src.users.model         import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# ── Config injection demo ─────────────────────────────────────
@router.get("/config", summary="Show injected config  (Topic: Config Injection)")
def show_config(
    settings: Settings = Depends(get_settings),   # ← config injected!
):

    return {
        "app_name":         settings.APP_NAME,
        "version":          settings.APP_VERSION,
        "debug":            settings.DEBUG,
        "default_pagesize": settings.DEFAULT_PAGE_SIZE,
        "max_pagesize":     settings.MAX_PAGE_SIZE,
        "db_type":          settings.DB_TYPE,
    }


# ── Standard CRUD ─────────────────────────────────────────────
@router.get("/", summary="List all users (paginated)")
def list_users(
    db:     FakeDatabase     = Depends(get_db),
    params: PaginationParams = Depends(get_pagination),
):
    return paginate_list(db.get_all_users(), params)


@router.post("/", status_code=201, summary="Create a new user")
def create_user(
    body: UserCreate,
    db:   FakeDatabase = Depends(get_db),
):
    return db.create_user(username=body.username, email=body.email)


@router.get("/{user_id}", summary="Get user by ID")
def get_user(
    user_id: int,
    db: FakeDatabase = Depends(get_db),
):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user
