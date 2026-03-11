from fastapi import Header, HTTPException, status
from typing import Optional


def verify_token(x_token: Optional[str] = Header(default=None)) -> str:
    """
    TOPIC: Depends() basics — dependency that can BLOCK a request.

    Add to any view:
        @router.delete("/{id}", dependencies=[Depends(verify_token)])

    Test header:
        X-Token: secret-day3-token
    """
    if x_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Token header is required",
        )
    if x_token != "secret-day3-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token. Use: secret-day3-token",
        )
    return x_token
