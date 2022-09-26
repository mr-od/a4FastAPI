from typing import Optional
from .models import Vendor
from .interfaces.repositories_interface import AuthRepositoryInterface, ProfileRepositoryInterface
from .interfaces.jwt_interface import JWTInterface
from .interfaces.password_service_interface import PasswordServiceInterface
from core.config import get_settings
from fastapi import HTTPException, status
from .schemas import Token, UpdateUserSchema


class AuthServices:

    def __init__(self, repository: AuthRepositoryInterface, password_service: PasswordServiceInterface):
        self._repository = repository
        self._password_service = password_service
        self._settings = get_settings()

    async def _authenticate(self, email: str, password: str):
        if not (vendor := await self._repository.get_vendor_by_email(email=email)) \
                or not await self._password_service.verify_password(plain_password=password, hashed_password=vendor.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
        return vendor

    async def login(self, email: str, password: str, token_service: JWTInterface) -> Token:
        vendor = await self._authenticate(email=email, password=password)
        subject = {'sub': vendor.email}
        access_token = await token_service.create_token_for_user(data=subject, secret_key=self._settings.secret_key,
                                                                 exp_time=self._settings.access_token_expire_minutes,
                                                                 algorithm=self._settings.algorithm)
        return Token(access_token=access_token, token_type='bearer')

    async def signup(self, email: str, username: str, password: str, is_admin: Optional[bool]):
        if await self._repository.get_vendor_by_email(email=email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Vendor with this email exists')
        if await self._repository.get_vendor_by_username(username=username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Vendor with this username exists')
        hashed_password = await self._password_service.get_hashed_password(password=password)
        return await self._repository.save_vendor(email=email, username=username, password=hashed_password, is_admin=is_admin)



class ProfileUserServices:

    def __init__(self, repository: ProfileRepositoryInterface):
        self._repository = repository

    async def get_vendor(self, vendor: Vendor):
        return await self._repository.get_vendor(vendor=vendor)

    async def update_vendor(self, vendor: Vendor, updated_data: UpdateUserSchema):
        data = updated_data.dict(exclude_none=True)
        return await self._repository.update_vendor(vendor=vendor, updated_data=data)

    async def delete_vendor(self, vendor: Vendor):
        return await self._repository.delete_vendor(vendor=vendor)