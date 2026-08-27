from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import favorite as crud_favorite
from app.schemas.favorite import FavoriteCreate,FavoriteResponse,FavoriteUserShow

router = APIRouter(prefix='/favorite', tags = ['Избранное'])


@router.post("/create", response_model=FavoriteResponse,status_code=status.HTTP_201_CREATED)
async def add_favorite(favorite: FavoriteCreate,db: AsyncSession = Depends(get_db)):
    return await crud_favorite.add_favorite(db, favorite)

@router.delete("/delete/{product_id}", status_code=status.HTTP_201_CREATED)
async def delete_favorite(favorite: FavoriteCreate,db: AsyncSession = Depends(get_db)):
    return await crud_favorite.delete_favorite(db, favorite)

@router.get('/get',response_model= FavoriteUserShow, status_code=status.HTTP_201_CREATED)
async def get_favorites(user_id:int, db: AsyncSession = Depends(get_db)):
    return await crud_favorite.get_favorite(db,user_id)