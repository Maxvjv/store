from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.favorite import FavoriteCreate,FavoriteProductShow,FavoriteUserShow
from app.models.user import User
from app.models.product import Product
from app.models.favorite import Favorite
from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload

#Добавление в избранное
async def add_favorite(db: AsyncSession,favorite:FavoriteCreate):
    result1 = await db.execute(select(User).where(User.id == favorite.user_id))
    db_user = result1.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code = 404, detail = 'Пользователь не найден')
    result2 = await db.execute(select(Product).where(Product.id == favorite.product_id))
    db_product = result2.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code = 404, detail = 'Продукт не найден')
    result3 = await db.execute(select(Favorite).where(Favorite.user_id == favorite.user_id,
                                                      Favorite.product_id == favorite.product_id))
    db_favorite = result3.scalar_one_or_none()
    if db_favorite:
        raise HTTPException(status_code = 404, detail = 'Продукт уже добавлен в избранное')
    db_favorite_user = Favorite(**favorite.model_dump())
    db.add(db_favorite_user)
    await db.commit()
    await db.refresh(db_favorite_user)
    return db_favorite_user

# Удаление из избранного
async def delete_favorite(db: AsyncSession,favorite:FavoriteCreate):
    result = await db.execute(select(Favorite).where(Favorite.user_id == favorite.user_id,
                                                     Favorite.product_id == favorite.product_id))
    db_favorite = result.scalar_one_or_none()
    if not db_favorite:
        raise HTTPException(status_code = 404, detail = 'Ошибка')
    await db.delete(db_favorite)
    await db.commit()
    return db_favorite

# Список товаров в избранном
async def get_favorite(db: AsyncSession, user_id: int):
    stmt = (
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .options(
            selectinload(Favorite.user),      # Подгружаем данные пользователя
            selectinload(Favorite.product)    # Подгружаем товары
        )
    )
    
    result = await db.execute(stmt)
    
    # ❌ БЫЛО: result.scalar_one_or_none() -> Вызывало MultipleResultsFound
    # ✅ СТАЛО: result.scalars().all() -> Возвращает СПИСОК всех записей Favorite
    favorites = result.scalars().all()
    
    if not favorites:
        # Если избранного нет, возвращаем пустой список.
        # Важно: берем пользователя отдельно, чтобы заполнить поле 'user'
        user_stmt = select(User).where(User.id == user_id) # Замени User на твою модель пользователя
        user_res = await db.execute(user_stmt)
        user_obj = user_res.scalars().first()
        
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
            
        return FavoriteUserShow(user=user_obj, product=[])

    # Берем данные первого пользователя (они одинаковы для всех записей этого юзера)
    user_data = favorites[0].user
    
    # ГЛАВНОЕ ИСПРАВЛЕНИЕ:
    # Мы должны создать список объектов FavoriteProductShow.
    # Каждый объект FavoriteProductShow принимает аргумент product=ProductORM
    formatted_products = [
        FavoriteProductShow(product=fav.product) 
        for fav in favorites
    ]
    
    return FavoriteUserShow(user=user_data, product=formatted_products)