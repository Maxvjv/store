from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import decode_token
from app.crud import user as crud_users
from app.database import get_db

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="not found user_id in token")

    user = await crud_users.get_user_id(int(user_id),db)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="not found user_id in token")

    user = await crud_users.get_user_id(int(user_id),db)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    elif user.role != 'admin':
        raise HTTPException(status_code=401, detail="У вас недостаточно прав")

    return user
