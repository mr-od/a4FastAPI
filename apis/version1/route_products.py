from fastapi import APIRouter, Depends, File, Form, status, UploadFile, responses
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from a4app.image_service.image_service import ImageOssService
from a4app.vendors.permissions import GetVendor
from a4app.users.permissions import GetUser

from a4app.vendors.token_service import TokenService
from a4app.products.services import ProductServices
from a4app.products.repositories import ProductsRepository
from typing import Optional
from core.config import get_settings
from a4app.products.schemas import CreateOrUpdateProductSchema, GadgetRSchema, GadgetSchema, ProductSchema
from a4app.products.update_schema import UpdateProductSchema
from a4app.vendors.models import Vendor
from a4app.users.models import User


products_routers = APIRouter()

#    //////////////////               Shopper App   /////////////////////////// #


@products_routers.get("/promoted", status_code=status.HTTP_200_OK, response_model=list[GadgetRSchema])
async def fetch_promoted_products(db: AsyncSession = Depends(get_db),
                                  #   current_user: User = Depends(GetUser(token_service=TokenService()))
                                  ) -> dict:
    """
    See all Promoted Products. This shows all the products promoted by afia4 on the homepage of the shopper.
    """
    return await ProductServices(repository=ProductsRepository(session=db)).get_promoted_products()


@products_routers.get("/active", status_code=status.HTTP_200_OK, response_model=list[GadgetRSchema])
async def fetch_active_products(db: AsyncSession = Depends(get_db), current_user: User = Depends(GetUser(token_service=TokenService()))) -> dict:
    """
    See all Active Products. This shows all the products active on afia4.
    """
    return await ProductServices(repository=ProductsRepository(session=db)).get_active_products()


#    //////////////////     Vendor App   /////////////////////////// #
@products_routers.get("/me", status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def read_own_products(db: AsyncSession = Depends(get_db), current_user: Vendor = Depends(GetVendor(token_service=TokenService()))) -> dict:
    """
    See all Current Active Vendor Products. This shows all the products of the currently logged in Vendor.
    """
    return await ProductServices(repository=ProductsRepository(session=db)).list_vendor_products(user=current_user.id)


@products_routers.post('/add-gadget', status_code=status.HTTP_201_CREATED, response_model=GadgetRSchema)
async def add_gadget(data: GadgetSchema = Depends(GadgetSchema.as_form),
                     files: Optional[list[UploadFile]] = File(None),
                     db: AsyncSession = Depends(get_db),
                     user: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProductServices(repository=ProductsRepository(session=db)) \
        .create_product(data=data, files=files, user=user, image_service=ImageOssService())


@products_routers.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_product(data: CreateOrUpdateProductSchema = Depends(CreateOrUpdateProductSchema.as_form),
                         files: Optional[list[UploadFile]] = File(None),
                         db: AsyncSession = Depends(get_db),
                         user: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProductServices(repository=ProductsRepository(session=db)) \
        .create_product(data=data, files=files, user=user, image_service=ImageOssService())


@products_routers.put('/{product_id}')
async def update_product(product_id: int,
                         updated_data: UpdateProductSchema = Depends(
                             UpdateProductSchema.as_form),
                         db: AsyncSession = Depends(get_db),
                         user: Vendor = Depends(GetVendor(token_service=TokenService()))):
    return await ProductServices(repository=ProductsRepository(session=db))\
        .update_product(product_id=product_id, data=updated_data, user=user)


@products_routers.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db),
                         user: Vendor = Depends(GetVendor(token_service=TokenService()))):
    await ProductServices(repository=ProductsRepository(session=db)) \
        .delete_product(product_id=product_id, user=user, image_service=ImageOssService())
    return {'detail': 'Product was deleted'}

# @products_routers.post('/favorites/{product_id}', status_code=status.HTTP_201_CREATED)
# async def add_to_favorites(product_id: int, db: AsyncSession = Depends(get_db),
#                            user: User = Depends(GetUser(token_service=TokenService()))):
#     result = await ProductServices(repository=ProductsRepository(session=db)).add_product_to_favorites(product_id=product_id, user=user)
#     if result:
#         return {'detail': 'Product has been added to favorites'}

# @products_routers.delete('/favorites/{favorite_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_from_favorites(favorite_id: int, db: AsyncSession = Depends(get_db),
#                                 user: User = Depends(GetUser(token_service=TokenService()))):
#     await ProductServices(repository=ProductsRepository(session=db)).remove_product_from_favorites(favorite_id=favorite_id, user=user)
#     return {'detail': 'Favorite product was deleted'}
