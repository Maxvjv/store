from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse
from sqlalchemy import select


#Создаём безопасный хэш пароля с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Создание пользователя
async def create_user(db: AsyncSession, user_data: UserCreate): 
    db_user = User(**user_data.model_dump())
    db_user.password = get_password_hash(db_user.password) 
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

#Вывод информации о всех пользователях
async def get_user(db:AsyncSession) -> list[User]:
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()

#Вывод информации об одном пользователе
async def get_user_id(user_id:int,db:AsyncSession) -> list[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code = 404, detail = 'Пользователь не найден')
    await db.commit()
    return user