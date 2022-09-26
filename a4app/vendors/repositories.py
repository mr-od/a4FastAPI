from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from .interfaces.repositories_interface import AuthRepositoryInterface, ProfileRepositoryInterface
from .models import Vendor


class AuthRepository(AuthRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_vendor(self, email: str, username: str, password: str, is_admin: bool = False):
        result = await self._session.execute(insert(Vendor).values(email=email, password=password, username=username, is_admin=is_admin).returning(Vendor))
        await self._session.commit()
        return result.first()

    async def get_vendor_by_email(self, email: str) -> Vendor:
        result = await self._session.execute(select(Vendor).where(Vendor.email ==email))
        return result.scalars().first()

    async def get_vendor_by_username(self, username: str) -> Vendor:
        result = await self._session.execute(select(Vendor).where(Vendor.username ==username))
        return result.scalars().first()    
    


class ProfileUserRepository(ProfileRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_vendor(self, vendor: Vendor) -> Vendor:
        result = await self._session.execute(select(Vendor).where(Vendor.id == vendor.id))
        return result.scalars().first()
        

    async def update_vendor(self, vendor: Vendor, updated_data: dict):
        result = await self._session.execute(update(Vendor).where(Vendor.id == vendor.id).values(**updated_data).returning(Vendor))
        await self._session.commit()
        return result.first()

    async def delete_user(self, user: Vendor):
        result = await self._session.execute(delete(Vendor).where(Vendor.id == user.id))
        await self._session.commit()
