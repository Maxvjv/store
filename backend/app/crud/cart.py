from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload,joinedload
from app.models.cart import Cart,CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartBase,CartCreate,CartItemBase,CartItemCreate,CartItemResponse
from sqlalchemy import delete,select

# Создание корзины
async def create_cart(db: AsyncSession, cart_data: CartCreate):
    result = await db.execute(select(User).where(User.id == cart_data.user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code = 404, detail = 'Пользователь не найден')
    db_cart = Cart(**cart_data.model_dump())
    db.add(db_cart)
    await db.commit()
    await db.refresh(db_cart)
    return db_cart


#Добавление товара в корзину
async def create_cartitem(db: AsyncSession, cartitem:CartItemCreate):
    result1 = await db.execute(select(Product).where(Product.id == cartitem.product_id))
    product1 = result1.scalar_one_or_none()
    if product1 and product1.stock > 0:
        result2 = await db.execute(select(Cart).where(Cart.id == cartitem.cart_id))
        db_cart = result2.scalar_one_or_none()
        if not db_cart:
            raise HTTPException(status_code = 404, detail = 'Корзина не найдена')
        result3 = await db.execute(select(CartItem).where(CartItem.cart_id == cartitem.cart_id,
                                                          CartItem.product_id == cartitem.product_id))
        db_cartitem = result3.scalar_one_or_none()
        if db_cartitem and product1.stock > db_cartitem.quantity:
            db_cartitem.quantity +=1
            await db.commit()
            await db.refresh(db_cartitem)
            return db_cartitem
        if not db_cartitem and product1.stock >=1:
            db_cart2 = CartItem(quantity = 1,**cartitem.model_dump())
            db.add(db_cart2)
            await db.commit()
            await db.refresh(db_cart2)
            return db_cart2
        else :
            raise HTTPException(status_code = 404, detail = 'Продукта нет на складе')   
    else:
        raise HTTPException(status_code = 404, detail = 'Продукта нет на складе')

# Изменить кол-во товара в корзине
async def put_product_cartitem(db:AsyncSession,user_id:int,product_id: int,quantity: int):
    result1 = await db.execute(select(Product).where(Product.id == product_id))
    product1 = result1.scalar_one_or_none()
    if product1.stock < quantity:
        raise HTTPException(status_code = 404, detail = f'Товара в кол-ве {quantity} нет на складе') 
    result2 = await db.execute(select(Cart).where(Cart.user_id == user_id))
    db_cart = result2.scalar_one_or_none()
    if not db_cart:
        raise HTTPException(status_code = 404, detail = 'Корзины нет')
    result3 = await db.execute(select(CartItem).where(CartItem.cart_id == db_cart.id,
                                                      CartItem.product_id == product_id))
    db_product = result3.scalar_one_or_none() 
    if not db_product:
        raise HTTPException(status_code = 404, detail = 'Такого товара нет в корзине')
    db_product.quantity = quantity
    await db.commit()
    await db.refresh(db_product)
    return db_product

#Список товаров в корзине пользователя
async def get_user_cartitem(db: AsyncSession, user_id:int):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.user),selectinload(Cart.cartitem).joinedload(CartItem.product)))                                                                                
    db_cart = result.scalar_one_or_none() 
    

    if not db_cart:
          raise HTTPException(status_code = 404, detail = 'Корзины нет')
     
                                                                                              
    return db_cart

# Удаление товара из корзины
async def delete_product_cartitem(db:AsyncSession,user_id:int,product_id:int):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    db_cart = result.scalar_one_or_none()
    if not db_cart:
        raise HTTPException(status_code = 404, detail = 'Корзины нет')
    result2 = await db.execute(select(CartItem).where(CartItem.cart_id == db_cart.id,
                                                      CartItem.product_id == product_id))
    db_product = result2.scalar_one_or_none() 
    if not db_product:
            raise HTTPException(status_code = 404, detail = 'Такого товара нет в корзине')
    await db.delete(db_product)
    await db.commit()
    return db_product

         
    
#Удаление всех товаров из корзины
async def delete_cartitem_all(db:AsyncSession,user_id:int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
            raise HTTPException(status_code = 404, detail = 'Пользователь не найден')
    result2 = await db.execute(select(Cart).where(Cart.user_id == user_id))
    db_cart = result2.scalar_one_or_none()
    print(db_cart.id)
    if not db_cart:
            raise HTTPException(status_code = 404, detail = 'Корзина пуста')
    result3 = delete(CartItem).where(CartItem.cart_id == db_cart.id)
    db_cartitem = await db.execute(result3)
    await db.delete(db_cart)
    await db.commit()
    return db_cartitem
