from fastapi import Depends, Query
from dataclasses import dataclass
from app.core.config import Settings, get_settings


@dataclass
class PaginationParams:
    page:   int
    size:   int
    offset: int


def get_pagination(
    page:     int      = Query(default=1,  ge=1,  description="Page number"),
    size:     int      = Query(default=10, ge=1,  description="Items per page"),
    settings: Settings = Depends(get_settings),
) -> PaginationParams:
    """
    TOPIC: Reusable Dependency
    Define ONCE → inject in items, products, users views.
    """
    size   = min(size, settings.MAX_PAGE_SIZE)
    offset = (page - 1) * size
    return PaginationParams(page=page, size=size, offset=offset)


def paginate_list(items: list, params: PaginationParams) -> dict:
    total       = len(items)
    sliced      = items[params.offset: params.offset + params.size]
    total_pages = max(1, (total + params.size - 1) // params.size)
    return {
        "items":       sliced,
        "total":       total,
        "page":        params.page,
        "size":        params.size,
        "total_pages": total_pages,
        "has_next":    params.page < total_pages,
        "has_prev":    params.page > 1,
    }
