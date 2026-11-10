from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.favorite import FavoriteCreate,FavoriteUserShow
from app.schemas.user import UserCartShow
from app.schemas.product import ProductFavoriteShow

from app.models.user import User
from app.models.product import Product
from app.models.favorite import Favorite
from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload

#Добавление в избранное
async def add_favorite(db: AsyncSession,favorite:FavoriteCreate,current_user:dict):
    result2 = await db.execute(select(Product).where(Product.id == favorite.product_id))
    db_product = result2.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code = 404, detail = 'Продукт не найден')
    result3 = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id,
                                                      Favorite.product_id == favorite.product_id))
    db_favorite = result3.scalar_one_or_none()
    if db_favorite:
        raise HTTPException(status_code = 404, detail = 'Продукт уже добавлен в избранное')
    db_favorite_user = Favorite(**favorite.model_dump())
    db_favorite_user.user_id = current_user.id
    db.add(db_favorite_user)
    await db.commit()
    await db.refresh(db_favorite_user)
    return db_favorite_user

# Удаление из избранного
async def delete_favorite(db: AsyncSession,prod_id:int,current_user:dict):
    result = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id,
                                                     Favorite.product_id == prod_id))
    db_favorite = result.scalar_one_or_none()
    if not db_favorite:
        raise HTTPException(status_code = 404, detail = 'Ошибка, нет такого товара в избранном')
    await db.delete(db_favorite)
    await db.commit()
    return db_favorite

# Список товаров в избранном
async def get_favorite(db: AsyncSession, current_user:dict)-> FavoriteUserShow:
   result = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id).options(
                                                    joinedload(Favorite.product)))
   favorites = result.scalars().all()
   if not favorites:
        raise HTTPException(status_code = 404, detail = 'В избранном пусто')

   products = [ProductFavoriteShow.model_validate(fav.product) for fav in favorites]

   return FavoriteUserShow(product=products)