from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import address as crud_address
from app.dependencies.auth import get_current_user

from app.schemas.address import AddressResponse,AddressCreate,AddressUpdate,AddressOrderShow

router = APIRouter(prefix='/address', tags = ['Адрес'])


@router.post("/create", response_model=AddressResponse,status_code=status.HTTP_201_CREATED)
async def create_address(address: AddressCreate, current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_address.create_address(address,current_user,db)

@router.patch('/update/{address_id}',response_model = AddressResponse,status_code=status.HTTP_200_OK)
async def update_address(address_data:AddressUpdate,address_id:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_address.update_address(address_data,address_id,current_user,db)

@router.get('/get/',response_model = list[AddressOrderShow],status_code=status.HTTP_200_OK)
async def get_list_address(current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_address.get_list_address(current_user,db)

@router.delete('/delete/{address_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id:int,current_user: dict = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return await crud_address.delete_address(address_id,current_user,db)