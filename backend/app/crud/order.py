from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete,select
from sqlalchemy.orm import selectinload,joinedload
from decimal import Decimal
from datetime import datetime


from app.schemas.order import OrderCreate,OrderItems,OrderStatusEnum


from app.models.user import User
from app.models.order import Order,OrderItem
from app.models.product import Product
from app.models.cart import Cart,CartItem
from app.models.address import Address
from app.models.promotion import PromotionProducts
from app.models.category import Category

from app.crud.cart import get_user_cartitem

#Создание заказа
async def create_order(db: AsyncSession,order:OrderCreate,current_user:dict):
    result2 = await db.execute(select(Address).where(Address.user_id == current_user.id,
                                                    Address.id == order.shipping_address))
    db_address = result2.scalar_one_or_none()
    if not db_address:
        raise HTTPException(status_code = 404, detail = 'Адреса для заказа нет в базе')
    result3 = await db.execute(select(Cart).where(Cart.user_id == current_user.id).options(
                                                    joinedload(Cart.cartitem).joinedload(CartItem.product)))
    db_cart = result3.unique().scalars().first()
    if not db_cart or not db_cart.cartitem:
        raise HTTPException(status_code = 404, detail = 'Корзина пуста,заказ нельзя создать')

    total_amount = Decimal("0.00")
    order_user = []

    cart_price = await get_user_cartitem(db,current_user)

    price_by_product = {
    item["product_id"]: item["final_unit_price"]
    for item in cart_price
}

    for ord in db_cart.cartitem:
        quantity = ord.quantity
        unit_price = price_by_product.get(ord.product.id, ord.product.price)
        price_prod = quantity * unit_price
        total_amount += price_prod

        if ord.product.stock < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара '{ord.product.name}': требуется {quantity}, доступно {ord.product.stock}"
            )

        order_user.append({
            'product_id': ord.product.id,
            'quantity': quantity,
            'price_at_time': price_prod,
            'product': ord.product,          
        })

    # Заказ 
    order_address = Order(
        user_id=current_user.id,
        status=OrderStatusEnum.pending,
        total_amount=total_amount,
        shipping_address=order.shipping_address,
        contact_phone=order.contact_phone,
    )
    db.add(order_address)
    await db.flush()                         

    # Позиции заказа
    for item in order_user:
        oi = OrderItem(
            order_id=order_address.id,       
            product_id=item["product_id"],
            quantity=item["quantity"],
            price_at_time=item["price_at_time"],
        )
        db.add(oi)

        
        item["product"].stock -= item["quantity"]

    await db.delete(db_cart)
    await db.commit()
    await db.refresh(order_address)

    return order_address

#Список заказов
async def get_order_list(db: AsyncSession,current_user: dict):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    db_order = result.unique().scalars().all()
    if not db_order:
        raise HTTPException(status_code = 404, detail = 'У пользователя нет заказов')
    return db_order

#Детали заказа
async def get_orderitems(db: AsyncSession,current_user: dict,order_id:int):                                           
    result = await db.execute(select(OrderItem)
        .join(Order)
        .where(OrderItem.order_id == order_id,Order.user_id == current_user.id)
        .options(joinedload(OrderItem.product)))
    db_orderitems = result.scalars().all()
    if not db_orderitems:
        raise HTTPException(status_code = 404, detail = 'У пользователя нет заказов')
    return db_orderitems
    

       

   