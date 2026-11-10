from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from app.models.user import User
from app.models.product import Product
from app.schemas.review import *
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload,joinedload

#Создание отзыва
async def create_review(db: AsyncSession,product_id : int,review_data: ReviewCreate,current_user:dict):
    result2 = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result2.scalar_one_or_none()
    if not db_product:
           raise HTTPException(status_code = 404, detail = 'Товара нет в системе') 
    result3 = await db.execute(select(Review).where(Review.user_id == current_user.id,
                                                   Review.product_id == product_id))
    db_review = result3.scalar_one_or_none()
    if db_review:
        raise HTTPException(status_code = 404, detail = 'Отзыв этим пользователем на этот продукт уже составлен')
    db_new_review = Review(**review_data.model_dump())
    db_new_review.user_id = current_user.id
    db_new_review.product_id = product_id
    if db_new_review.rating >= 1 and db_new_review.rating <= 5:
        db.add(db_new_review)
        await db.commit()
        await db.refresh(db_new_review)
        await sred_review(db,product_id)
        return db_new_review
    
    else:
        raise HTTPException(status_code = 404, detail = 'Рейтинг должен быть в диапозоне от 1 до 5')
    
#Обновление отзыва
async def update_review(db: AsyncSession, review_data:ReviewUpdate, current_user:dict):
    result = await db.execute(select(Review).where(Review.product_id == review_data.product_id,
                                                   Review.user_id == current_user.id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code = 404, detail = 'Отзыв не найден')
    if review_data.rating >= 1 and review_data.rating <=5:
        update_data = review_data.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(review,key,value)

        await db.commit()
        await db.refresh(review)
        await sred_review(db,review.product_id)
        return review
    else:
        raise HTTPException(status_code = 404, detail = 'Рейтинг должен быть в диапозоне от 1 до 5')

#Подсчет среднего рейтинга
async def sred_review(db:AsyncSession,product_id:int):
    result = await db.execute(select(func.avg(Review.rating)).where(Review.product_id == product_id))
    db_review = result.scalar_one_or_none()
    if not db_review:
        return None
    result2 = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result2.scalar_one_or_none()
    db_product.average_rating = round(db_review,1)
    await db.commit()
    await db.refresh(db_product)
    return db_product



# Удаление отзыва
async def delete_review(db:AsyncSession,product_id:int, current_user:dict):
    result = await db.execute(select(Review).where(Review.product_id == product_id,
                                                       Review.user_id == current_user.id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code = 404, detail = 'Отзыв не найден')
    await db.delete(review)
    await db.commit()
    await sred_review(db,review.product_id)
    raise HTTPException(status_code = 204,detail = 'Отзыв удален')

#Список отзывов на товар
async def get_review(db:AsyncSession,product_id:int):
    result1 = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result1.scalar_one_or_none()
    print (db)
    if not db_product:
         raise HTTPException(status_code = 404, detail = 'Такого товара нет')
    result2 = await db.execute(select(Review).where(Review.product_id == product_id).options(
                                                    joinedload(Review.user)
    ))
    db_review = result2.scalars().all()
    reviews_show = [
        ReviewUserShow(
            user=UserReviewShow.model_validate(r.user),
            rating=r.rating,
            comment=r.comment,      
        )
        for r in db_review
    ]

    return ReviewProductShow(product=ProductReviewShow.model_validate(db_product),reviews=reviews_show,)