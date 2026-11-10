from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload

from app.models.promotion import Promotion,PromotionProducts,PromotionCategories
from app.models.product import Product
from app.models.category import Category
from app.schemas.promotion import PromotionCreate,PromoProductCreate,PromoCategoryCreate

async def create_promotion(db: AsyncSession, promotion_data: PromotionCreate):
    db_promotion = Promotion(**promotion_data.model_dump())
    db.add(db_promotion)
    await db.commit()
    await db.refresh(db_promotion)
    return db_promotion

async def create_promo_prod(db: AsyncSession,promo_prod : PromoProductCreate):
    result1 = await db.execute(select(Promotion).where(Promotion.id == promo_prod.promotion_id))
    db_promo = result1.scalar_one_or_none()
    if not db_promo:
       raise HTTPException(status_code = 404, detail = 'Акция отсутствует')
    result2 = await db.execute(select(Product).where(Product.id == promo_prod.product_id))
    db_prod = result2.scalar_one_or_none()
    if not db_prod:
       raise HTTPException(status_code = 404, detail = 'Такого товара нет')
    result3 = await db.execute(select(PromotionProducts).where(PromotionProducts.promotion_id == promo_prod.promotion_id,
                                                                    PromotionProducts.product_id == promo_prod.product_id))
    db_promo_prod = result3.scalar_one_or_none()
    if db_promo_prod:
       raise HTTPException(status_code = 404, detail = 'Акция уже применяется к данному товару')
    if db_promo.applicable_to == 'product':
        db_promotion = PromotionProducts(**promo_prod.model_dump())
        db.add(db_promotion)
        await db.commit()
        await db.refresh(db_promotion)
        return db_promotion
    else:
      raise HTTPException(status_code = 404, detail = 'Акция предназначена к категории, к продукту применить нельзя')

async def create_promo_cat(db: AsyncSession,promo_cat : PromoCategoryCreate):
    result1 = await db.execute(select(Promotion).where(Promotion.id == promo_cat.promotion_id))
    db_promo = result1.scalar_one_or_none()
    if not db_promo:
       raise HTTPException(status_code = 404, detail = 'Акция отсутствует')
    result2 = await db.execute(select(Category).where(Category.id == promo_cat.category_id))
    db_cat = result2.scalar_one_or_none()
    if not db_cat:
       raise HTTPException(status_code = 404, detail = 'Такой категории нет')
    result3 = await db.execute(select(PromotionCategories).where(PromotionCategories.promotion_id == promo_cat.promotion_id,
                                                                    PromotionCategories.category_id == promo_cat.category_id))
    db_promo_prod = result3.scalar_one_or_none()
    if db_promo_prod:
       raise HTTPException(status_code = 404, detail = 'Акция уже применяется к данной категории')
    if db_promo.applicable_to == 'category':
        db_promotion = PromotionCategories(**promo_cat.model_dump())
        db.add(db_promotion)
        await db.commit()
        await db.refresh(db_promotion)
        return db_promotion
    else:
      raise HTTPException(status_code = 404, detail = 'Акция предназначена к продукту, к категории применить нельзя')

