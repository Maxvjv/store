from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import user as crud_user
from app.dependencies.auth import get_current_admin,get_current_user
from app.schemas.user import UserCreate,UserResponse,UserRegistration

router = APIRouter(prefix='/users', tags = ['Пользователи'])

@router.post("/create", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate,db: AsyncSession = Depends(get_db)):
    return await crud_user.create_user(db, user)

@router.post("/registration", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def registration_user(user: UserRegistration,db: AsyncSession = Depends(get_db)):
    return await crud_user.registration_user(db, user)

@router.get('/list',response_model=list[UserResponse],status_code=status.HTTP_200_OK)
async def get_user(db: AsyncSession = Depends(get_db),current_user: dict = Depends(get_current_admin)):
    return await crud_user.get_user(db,current_user)

@router.get('/list/me',response_model = UserResponse,status_code=status.HTTP_200_OK)
async def get_my_user(current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_user.get_my_user(current_user,db)