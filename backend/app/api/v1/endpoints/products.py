from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix='/product', tags = ['Продукты'])


@router.post("/create", response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate,db: AsyncSession = Depends(get_db)):
    return await crud_product.create_product(db, product)

@router.get('/list')
async def get_product(skip:int = 0,
                      limit:int = 100, 
                      sort_by: str = 'id', 
                      order:str = 'asc',
                      db: AsyncSession = Depends(get_db)):
    return await crud_product.get_product(db,skip,limit,sort_by,order)

@router.patch('/update/{product_id}',response_model = ProductResponse)
async def update_product(product_id:int, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await crud_product.update_product(db,product_id,product_data)

@router.delete('/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_product.delete_product(db,product_id)