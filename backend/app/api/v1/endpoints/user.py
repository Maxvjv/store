from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate,UserResponse

router = APIRouter(prefix='/users', tags = ['Пользователи'])

@router.post("/create", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate,db: AsyncSession = Depends(get_db)):
    return await crud_user.create_user(db, user)

@router.get('/list',response_model=list[UserResponse],status_code=status.HTTP_201_CREATED)
async def get_user(db: AsyncSession = Depends(get_db)):
    return await crud_user.get_user(db)

@router.get('/list/{user_id}',response_model = UserResponse,status_code=status.HTTP_201_CREATED)
async def get_user_id(user_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_user.get_user_id(user_id,db)