from __future__ import annotations

import uuid
from typing import Annotated

import jwt  # type: ignore[import-not-found]
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SETTINGS
from app.core.depends.get_session import get_session
from app.crud.user import UserCrud
from app.model.model import User

security_scheme = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SETTINGS.JWT_SECRET, algorithms=[SETTINGS.JWT_ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise ValueError("Missing sub claim")
        user_id = uuid.UUID(subject)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = await UserCrud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
