
from fastapi import APIRouter, status, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from a4app.vendors.services import AuthServices, ProfileUserServices
from a4app.vendors.repositories import AuthRepository, ProfileUserRepository
from core.database import get_db
from a4app.vendors.schemas import CreateUserSchema, LoginUserSchema, Token, UserSchema, UpdateUserSchema
from a4app.vendors.password_service import PasswordService
from a4app.vendors.token_service import TokenService
from a4app.vendors.permissions import GetVendor
from a4app.vendors.models import Vendor

vendors_routers = APIRouter()


# auth controllers

@vendors_routers.post('/loginv', status_code=status.HTTP_200_OK, response_model=Token)
async def login(vendor_data: LoginUserSchema = Depends(LoginUserSchema.as_form), db: AsyncSession = Depends(get_db)):
    return await AuthServices(repository=AuthRepository(session=db),
                              password_service=PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))) \
        .login(**vendor_data.dict(exclude={'is_admin'}), token_service=TokenService())


@vendors_routers.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def signup(vendor_data: CreateUserSchema, db: AsyncSession = Depends(get_db)):
    return await AuthServices(repository=AuthRepository(session=db),
                              password_service=PasswordService(context=CryptContext(schemes=["bcrypt"], deprecated="auto"))) \
        .signup(**vendor_data.dict(exclude_none=True))


# profile controllers

@vendors_routers.get('/me', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_vendor_profile(db: AsyncSession = Depends(get_db), vendor: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).get_vendor(vendor=vendor)


@vendors_routers.put('/', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update_profile(updated_data: UpdateUserSchema, db: AsyncSession = Depends(get_db), vendor: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).update_user(vendor=vendor, updated_data=updated_data)


@vendors_routers.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(db: AsyncSession = Depends(get_db), vendor: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProfileUserServices(repository=ProfileUserRepository(session=db)).delete_user(vendor=vendor)
