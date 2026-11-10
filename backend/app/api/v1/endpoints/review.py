from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import review as crud_review
from app.schemas.review import *
from app.dependencies.auth import get_current_user

router = APIRouter(prefix='/review', tags = ['Отзывы'])


@router.post("/create/{product_id}", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
async def create_review(product_id : int,review_data: ReviewCreate,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_review.create_review(db, product_id, review_data,current_user)

@router.patch('/update/{product_id}',response_model = ReviewResponse,status_code=status.HTTP_200_OK)
async def update_review(review_data: ReviewUpdate, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud_review.update_review(db,review_data,current_user)

@router.delete('/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(product_id:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_review.delete_review(db,product_id,current_user)

@router.get('/get/{product_id}',response_model= ReviewProductShow, status_code=status.HTTP_200_OK)
async def get_review(product_id:int, db: AsyncSession = Depends(get_db)):
    return await crud_review.get_review(db,product_id)