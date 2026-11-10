from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order,OrderItem
from app.schemas.product import ProductCreate,ProductUpdate
from sqlalchemy import select,func


async def create_product(db: AsyncSession, product_data: ProductCreate,current_user:dict):
    result = await db.execute(select(Category).where(Category.id == product_data.category_id))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code = 404, detail = 'Категория не найдена')
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Весь список продуктов
async def get_product(db:AsyncSession,
                      skip: int = 0,
                      limit: int = 100,
                      sort_by:str | None = None,
                      order: str = 'asc')-> list[Product]:
    stmt = select(Product)

    sort_column = getattr(Product,sort_by,Product.id)

    if order == 'desc':
        stmt = stmt.order_by(sort_column.desc())
    else:
       stmt = stmt.order_by(sort_column.asc())     

    if skip:
        stmt = stmt.offset(skip)
    if limit:
        stmt = stmt.limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()

#Детальная информация о продукте
async def get_product_id(product_id:int,db:AsyncSession):
    result = await db.execute(select(Product).where(Product.id == product_id))
    prod = result.scalar_one_or_none()
    if not prod:
         raise HTTPException(status_code =555, detail = 'Нет такого товара')
    return prod

#Редактирование продукта(Обновление только переданных полей)
async def update_product(db: AsyncSession,product_id:int, product_data:ProductUpdate,current_user:dict):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code = 404, detail = 'Продукт не найден')
    update_data = product_data.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(product,key,value)
    
    await db.commit()
    await db.refresh(product)
    return product

# Удаление продукта
async def delete_product(db:AsyncSession,product_id:int,current_user:dict):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code = 404, detail = 'Продукт не найден')
    await db.delete(product)
    await db.commit()
    raise HTTPException(status_code = 204,detail = 'No content')


