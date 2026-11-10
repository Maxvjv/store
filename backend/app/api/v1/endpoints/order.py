from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import order as crud_order
from app.dependencies.auth import get_current_user
from app.schemas.order import OrderCreate,OrderResponse,OrderListShow,OrderItemsShow

router = APIRouter(prefix='/order', tags = ['Заказ'])

@router.post("/create", response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_order.create_order(db, order,current_user)

@router.get("/get_list_order", response_model=list[OrderListShow],status_code=status.HTTP_200_OK)
async def get_order_list(current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_order.get_order_list(db, current_user)

@router.get("/get_orderitems/{order_id}", response_model=list[OrderItemsShow],status_code=status.HTTP_200_OK)
async def get_orderitems(order_id:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_order.get_orderitems(db,current_user,order_id)