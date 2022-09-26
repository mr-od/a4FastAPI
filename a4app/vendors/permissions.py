from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from a4app.vendors.models import Vendor
from core.database import get_db
from core.config import get_settings
from a4app.vendors.interfaces.jwt_interface import JWTInterface


from sqlalchemy import select



class GetVendor:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/loginv')

    def __init__(self, token_service: JWTInterface):
        self._token_service = token_service
        self._settings = get_settings()

    async def _decode_token(self, token: str) -> str:
        payload: dict = await self._token_service.decode_token(token=token, secret_key=self._settings.secret_key, algorithm=self._settings.algorithm)
        return payload.get('sub')  # return email

    async def __call__(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_db)):
        email = await self._decode_token(token=token)
        result = await session.execute(select(Vendor).where(Vendor.email == email, Vendor.is_active))
        return result.scalars().first()

    async def get_admin_vendor(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_db)):
        email = await self._decode_token(token=token)
        result = await session.execute(select(Vendor).where(Vendor.email == email, Vendor.is_active, Vendor.is_admin))
        if not (vendor := result.scalars().first()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You are not an admin")