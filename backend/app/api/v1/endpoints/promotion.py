from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

from app.crud import promotion as crud_promotion
from app.schemas.promotion import PromotionCreate,PromoProductCreate,PromoCategoryCreate

router = APIRouter(prefix='/promotion', tags = ['Акции'])


@router.post("/create")
async def create_promotion(promotion_data: PromotionCreate,db: AsyncSession = Depends(get_db)):
    return await crud_promotion.create_promotion(db, promotion_data)

@router.post("/create/promo_prod")
async def create_promo_prod(promo_prod: PromoProductCreate,db: AsyncSession = Depends(get_db)):
    return await crud_promotion.create_promo_prod(db, promo_prod)

@router.post("/create/promo_cat")
async def create_promo_cat(promo_cat: PromoCategoryCreate,db: AsyncSession = Depends(get_db)):
    return await crud_promotion.create_promo_cat(db, promo_cat)



