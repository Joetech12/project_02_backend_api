
from typing import Annotated

from fastapi import Depends, Query


def get_app_info():
    return {
        "application": "Python Backend API",
        "version": "1.0.0",
    }


def pagination_params(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {
        "limit": limit,
        "offset": offset,
    }


Pagination = Annotated[
    dict,
    Depends(pagination_params),
]

AppInfo = Annotated[
    dict,
    Depends(get_app_info),
]

def get_current_user():
    return {
        "id": 1,
        "name": "Ifeanyi",
        "role": "admin",
    }


def require_admin(
    current_user: Annotated[
        dict,
        Depends(get_current_user),
    ],
):
    if current_user["role"] != "admin":
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )

    return current_user