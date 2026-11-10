from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload,joinedload
from decimal import Decimal
from datetime import datetime
from app.models.cart import Cart,CartItem
from app.models.product import Product
from app.models.user import User
from app.models.category import Category
from app.models.promotion import Promotion,PromotionProducts,PromotionCategories,Type
from app.schemas.cart import CartBase,CartCreate,CartItemBase,CartItemCreate,CartItemResponse
from sqlalchemy import delete,select,and_, or_

# Создание корзины
async def create_cart(db: AsyncSession, cartitem:CartItemCreate, current_user:User):
    result = await db.execute(
        select(Cart).where(Cart.user_id == current_user.id)
    )
    db_cart = result.scalar_one_or_none()
    if not db_cart:
        db_cart = Cart(user_id = current_user.id)
        db.add(db_cart)
        await db.flush()

    result1 = await db.execute(select(Product).where(Product.id == cartitem.product_id))
    product1 = result1.scalar_one_or_none()
    if product1 and product1.stock > 0:
        result3 = await db.execute(select(CartItem).where(CartItem.cart_id == db_cart.id,
                                                          CartItem.product_id == cartitem.product_id))
        db_cartitem = result3.scalar_one_or_none()
        if db_cartitem and product1.stock > db_cartitem.quantity:
            db_cartitem.quantity +=1
            await db.commit()
            await db.refresh(db_cartitem)
            return db_cartitem
        if not db_cartitem and product1.stock >=1:
            db_cart2 = CartItem(quantity = 1,**cartitem.model_dump())
            db_cart2.cart_id = db_cart.id
            db.add(db_cart2)
            await db.commit()
            await db.refresh(db_cart2)
            return db_cart2
        else :
            raise HTTPException(status_code = 404, detail = 'Продукта нет на складе')   
    else:
        raise HTTPException(status_code = 404, detail = 'Продукта нет на складе')

# Изменить кол-во товара в корзине
async def put_product_cartitem(db:AsyncSession,current_user:dict,product_id: int,quantity: int):
    result1 = await db.execute(select(Product).where(Product.id == product_id))
    product1 = result1.scalar_one_or_none()
    if product1.stock < quantity:
        raise HTTPException(status_code = 404, detail = f'Товара в кол-ве {quantity} нет на складе') 
    result2 = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
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
async def get_user_cartitem(db: AsyncSession, current_user:dict):
    now = datetime.now()
    result = await db.execute(
        select(Cart)
        .where(Cart.user_id == current_user.id)
        .options(joinedload(Cart.cartitem).joinedload(CartItem.product))
    )
    cart = result.unique().scalars().first()

    if not cart or not cart.cartitem:
        raise HTTPException(status_code = 404, detail = 'Корзины нет')


    product_ids = []
    category_ids = []

    for item in cart.cartitem:
        product_ids.append(item.product.id)
        category_ids.append(item.product.category_id)
    

    result2 = await db.execute (
        select(
            Promotion,
            PromotionProducts.product_id.label("p_product_id"),
            PromotionCategories.category_id.label("p_category_id"),
        )
        .where(
            and_(
                Promotion.is_active == True,
                Promotion.start_date <= now,
                Promotion.end_date >= now,
            )
        )
        .outerjoin(
            PromotionProducts,
            PromotionProducts.promotion_id == Promotion.id,
        )
        .outerjoin(
            PromotionCategories,
            PromotionCategories.promotion_id == Promotion.id,
        )
        .where(
            or_(
                PromotionProducts.product_id.in_(product_ids),
                PromotionCategories.category_id.in_(category_ids),
            )
        )
    )
    db_promo = result2.all()

    result_items = []
    
    for item in cart.cartitem:
        product = item.product
        unit_price = product.price
        best_price = unit_price
        best_promo = None

        for promo, p_product_id, p_category_id in db_promo:
            if p_product_id == product.id or p_category_id == product.category_id:
                candidate = price_with_type(unit_price, promo)
                if candidate < best_price:
                    best_price = candidate
                    best_promo = promo

        line_total = best_price * item.quantity
        line_total_no_discount = unit_price * item.quantity
        discount_amount = line_total_no_discount - line_total

        result_items.append({
            "cart_item_id": item.id,
            "quantity": item.quantity,
            "product_id": product.id,
            "product_name": product.name,
            "original_unit_price": unit_price,
            "final_unit_price": best_price,
            "line_total": line_total,
            "line_total_no_discount": line_total_no_discount,
            "discount_amount": discount_amount,
            "promotion_id": best_promo.id if best_promo else None,
            "promotion_name": best_promo.name if best_promo else None,
            "promotion_discount_type": (
                best_promo.discount_type.value
                if best_promo and hasattr(best_promo.discount_type, "value")
                else str(best_promo.discount_type) if best_promo else None
            ),
            "promotion_discount_value": best_promo.discount_value if best_promo else None,
        })

    return result_items

def price_with_type(price: Decimal, promo) -> Decimal:
    if promo.discount_type == Type.PERCENTAGE:
        return price * (Decimal(1) - promo.discount_value / Decimal(100))
    elif promo.discount_type == Type.FIXED:
        return max(price - promo.discount_value, Decimal(0))
    return price


# Удаление товара из корзины
async def delete_product_cartitem(db:AsyncSession,current_user:dict,product_id:int):
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    db_cart = result.scalar_one_or_none()
    if not db_cart:
        raise HTTPException(status_code = 404, detail = 'Корзины нет')
    result2 = await db.execute(select(CartItem).where(CartItem.cart_id == db_cart.id,
                                                      CartItem.product_id == product_id))
    db_product = result2.scalar_one_or_none() 
    if not db_product:
            raise HTTPException(status_code = 404, detail = 'Такого товара нет в корзине')
    if db_product.quantity == 1:
        await db.delete(db_product)
        await db.commit()
        return db_product
    db_product.quantity = db_product.quantity - 1
    await db.commit()
    return db_product
    

         
    
#Удаление всех товаров из корзины
async def delete_cartitem_all(db:AsyncSession,current_user:dict):
    result2 = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    db_cart = result2.scalar_one_or_none()
    if not db_cart:
            raise HTTPException(status_code = 404, detail = 'Корзина пуста')
    await db.delete(db_cart)
    await db.commit()
    raise HTTPException(status_code = 204, detail = 'No content')
