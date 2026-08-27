from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.category import Category
from app.schemas.category import CategoryCreate,CategoryUpdate

#Создание категории
async def create_category(db: AsyncSession, category_data: CategoryCreate):
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

#Список всех категорий
async def get_category(db:AsyncSession) -> list[Category]:
    stmt = select(Category).options(selectinload(Category.products))
    result = await db.execute(stmt)
    return result.scalars().all()

# Информация по конкретной категории
async def get_category_id(category_id:int,db:AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id).options(selectinload(Category.products)))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code = 404, detail = 'Категория не найдена')
    await db.commit()
    return category

#Редактирование Категории
async def update_category(db: AsyncSession,category_id:int, category_data:CategoryUpdate):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code = 404, detail = 'Категория не найдена')
    update_data = category_data.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(category,key,value)
    
    await db.commit()
    await db.refresh(category)
    return category

# Удаление категории
async def delete_category(db:AsyncSession,category_id:int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code = 404, detail = 'Продукт не найден')
    await db.delete(category)
    await db.commit()
    raise HTTPException(status_code = 204,detail = 'No content')