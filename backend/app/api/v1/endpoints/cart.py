from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import cart as crud_cart
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.cart import CartCreate,CartResponse,CartItemCreate, CartItemResponse,CartShowWithUser

router = APIRouter(prefix='/cart', tags = ['Корзина'])

@router.post("/create", response_model=CartResponse,status_code=status.HTTP_201_CREATED)
async def create_cart(cartitem:CartItemCreate ,current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_cart.create_cart(db, cartitem, current_user)

@router.get("/get/cart")
async def get_user_cartitem(current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_cart.get_user_cartitem(db, current_user)

@router.put("/put/items/{product_id}",status_code=status.HTTP_201_CREATED)
async def put_product_cartitem(product_id:int,quantity:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_cart.put_product_cartitem(db,current_user,product_id,quantity)

@router.delete('/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_cartitem(product_id:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_cart.delete_product_cartitem(db, current_user, product_id)

@router.delete('/delete-cart/all',status_code=status.HTTP_204_NO_CONTENT)
async def delete_cartitem_all(current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_cart.delete_cartitem_all(db, current_user)