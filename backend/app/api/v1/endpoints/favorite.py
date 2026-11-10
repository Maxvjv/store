from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import favorite as crud_favorite
from app.schemas.favorite import FavoriteCreate,FavoriteResponse,FavoriteUserShow
from app.dependencies.auth import get_current_user

router = APIRouter(prefix='/favorite', tags = ['Избранное'])


@router.post("/create", response_model=FavoriteResponse,status_code=status.HTTP_201_CREATED)
async def add_favorite(favorite: FavoriteCreate,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_favorite.add_favorite(db, favorite,current_user)

@router.delete("/delete/{prod_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(prod_id:int, current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_favorite.delete_favorite(db, prod_id,current_user)

@router.get('/get',response_model= FavoriteUserShow, status_code=status.HTTP_200_OK)
async def get_favorites(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    favorite = await crud_favorite.get_favorite(db,current_user)
    return favorite