from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate,UserResponse
from app.database import get_db
from app.security import create_access_token,create_refresh_token,decode_token,get_current_ip
from app.crud import user as crud_users

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login",response_model=TokenResponse)
async def login(login_data: LoginRequest,request: Request, db: AsyncSession = Depends(get_db)):
    user = await crud_users.authenticate_user(login_data.email, login_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    current_ip = get_current_ip(request)
    access_token = create_access_token({'id':user.id,'email':user.email})
    refresh_token = create_refresh_token({'id':user.id,'ip':current_ip})

    return TokenResponse(access_token = access_token,refresh_token = refresh_token)