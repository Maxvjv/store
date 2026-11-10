from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload,joinedload
from sqlalchemy import delete,select

from app.schemas.address import AddressCreate,AddressUpdate
from app.models.address import Address
from app.models.user import User


#Создание адреса
async def create_address(address:AddressCreate, current_user:dict, db: AsyncSession):
    db_address = Address(**address.model_dump())
    db_address.user_id = current_user.id
    db.add(db_address)
    await db.commit()
    await db.refresh(db_address)
    return db_address

#Редактирование адреса
async def update_address(address_data:AddressUpdate,address_id:int, current_user:dict,db: AsyncSession):
    result = await db.execute(select(Address).where(Address.id == address_id,
                                                    Address.user_id == current_user.id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code = 404, detail = 'Адрес не найден')
    update_data = address_data.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(address,key,value)
    
    await db.commit()
    await db.refresh(address)
    return address

#Список всех адресов пользователя
async def get_list_address(current_user:dict,db: AsyncSession):
    result = await db.execute(select(Address).where(Address.user_id == current_user.id))
    db_address = result.scalars().all()
    if not db_address:
            raise HTTPException(status_code = 404, detail = 'Список адресов пуст')
    return db_address

#Удаление Адреса
async def delete_address(address_id:int,current_user:dict,db:AsyncSession):
    result = await db.execute(select(Address).where(Address.id == address_id,
                                                    Address.user_id == current_user.id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code = 404, detail = 'Адрес не найден')
    await db.delete(address)
    await db.commit()
    return address