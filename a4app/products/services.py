from fastapi import HTTPException, UploadFile, status
from a4app.image_service.interfaces.service import ImageOssServiceInterface
from a4app.users.models import User
from a4app.vendors.models import Vendor
from .interfaces.repositories_interface import RepositoriesInterface
from typing import Optional
from .schemas import CreateOrUpdateProductSchema


class ProductServices:
    def __init__(self, repository: RepositoriesInterface):
        self._repository = repository

    # async def get_all_products(self, limit: Optional[int], offset: Optional[int],
    #                            query_data: QueryProductSchema):
    #     return await self._repository.get_all_products(limit=limit, offset=offset,
    #                                                    query_data=query_data.dict(exclude_none=True))

    # async def get_detail_product(self, product_id: int):
    #     return await self._repository.get_detail_product(product_id=product_id)

    async def get_promoted_products(self):
        return await self._repository.get_promoted_products()

    async def get_active_products(self):
        return await self._repository.get_active_products()

    async def list_vendor_products(self, user: Vendor):
        return await self._repository.list_vendor_products(user=user)

    async def delete_product(self, product_id: int, user: User, image_service: ImageOssServiceInterface):
        await self._repository.delete_product(product_id=product_id, user=user, image_service=image_service)

    async def create_product(self, data: CreateOrUpdateProductSchema,
                             files: Optional[list[UploadFile]], user: Vendor, image_service: ImageOssServiceInterface):
        created_data = data.dict(exclude_none=True)
        return await self._repository.create_product(product_data=created_data, user=user, files=files, image_service=image_service)

    async def update_product(self, product_id: int, data: CreateOrUpdateProductSchema, user: User,
                             ):
        updated_data = data.dict(exclude_none=True)
        result, product = await self._repository.update_product(product_id=product_id, user=user, updated_data=updated_data,
                                                                )
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='You cannot update this product')
        return product

    async def get_favorites_product(self, limit: Optional[int], offset: Optional[int], user: User):
        return await self._repository.get_favorite_products(offset=offset, limit=limit, user=user)

    async def add_product_to_favorites(self, product_id: int, user: User):
        return await self._repository.add_product_to_favorites(product_id=product_id, user=user)

    async def remove_product_from_favorites(self, favorite_id: int, user: User):
        return await self._repository.remove_product_from_favorites(favorite_id=favorite_id, user=user)
