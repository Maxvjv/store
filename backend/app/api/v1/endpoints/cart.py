from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import cart as crud_cart
from app.schemas.cart import CartCreate,CartResponse,CartItemCreate, CartItemResponse,CartShowWithUser

router = APIRouter(prefix='/cart', tags = ['Корзина'])

@router.post("/create", response_model=CartResponse,status_code=status.HTTP_201_CREATED)
async def create_cart(cart: CartCreate,db: AsyncSession = Depends(get_db)):
    return await crud_cart.create_cart(db, cart)

@router.post("/createitem", response_model=CartItemResponse,status_code=status.HTTP_201_CREATED)
async def create_cartitem(cartitem: CartItemCreate,db: AsyncSession = Depends(get_db)):
    return await crud_cart.create_cartitem(db, cartitem)

@router.get("/get/cart",response_model= CartShowWithUser,status_code=status.HTTP_201_CREATED)
async def get_user_cartitem(user_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_cart.get_user_cartitem(db, user_id)

@router.put("/put/items/{product_id}",status_code=status.HTTP_201_CREATED)
async def put_product_cartitem(user_id:int,product_id:int,quantity:int,db: AsyncSession = Depends(get_db)):
    return await crud_cart.put_product_cartitem(db,user_id,product_id,quantity)

@router.delete('/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_cartitem(user_id:int, product_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_cart.delete_product_cartitem(db, user_id, product_id)

@router.delete('/delete/all',status_code=status.HTTP_204_NO_CONTENT)
async def delete_cartitem_all(user_id:int,db: AsyncSession = Depends(get_db)):
    return await crud_cart.delete_cartitem_all(db, user_id)