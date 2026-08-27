from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryCreate,CategoryResponse,CategoryUpdate,CategoryWithProduct

router = APIRouter(prefix='/category', tags = ['Категории'])

@router.post("/create", response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate,db: AsyncSession = Depends(get_db)):
    return await crud_category.create_category(db, category)

@router.get('/list',response_model=list[CategoryWithProduct],status_code=status.HTTP_201_CREATED)
async def get_category(db: AsyncSession = Depends(get_db)):
    return await crud_category.get_category(db)

@router.get('/list/{category_id}',response_model=CategoryWithProduct,status_code=status.HTTP_201_CREATED)
async def get_category_id(category_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_category.get_category_id(category_id,db)

@router.patch('/update/{category_id}',response_model = CategoryResponse)
async def update_category(category_id:int, category_data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    return await crud_category.update_category(db,category_id,category_data)

@router.delete('/delete/{category_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_category.delete_category(db,category_id)