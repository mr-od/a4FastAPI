import secrets
from typing import Optional
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from a4app.users.models import User
from a4app.vendors.models import Vendor
from .interfaces.repositories_interface import RepositoriesInterface
from .models import Product
from fastapi import HTTPException, UploadFile, status
from a4app.image_service.interfaces.service import ImageOssServiceInterface
import uuid


class ProductsRepository(RepositoriesInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_product(self, product_id: int) -> Product:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        if not (product := result.scalars().first()):
            raise HTTPException(detail='Product not found',
                                status_code=status.HTTP_404_NOT_FOUND)
        return product

    async def get_all_products(self, limit: Optional[int], offset: Optional[int], query_data: dict, price_query_data: dict):
        stmt = select(Product).where(Product.is_active)
        stmt = await self._filter_result(stmt=stmt, data=query_data, price_data=price_query_data)
        result = await self._session.execute(stmt.limit(limit).offset(offset).order_by(Product.updated.desc()))
        return result.scalars().unique().all()

    async def get_detail_product(self, product_id: int) -> Product:
        return await self._get_product(product_id=product_id)

    async def imghex(filename: str):
        extension = await filename.split(".")[1]
        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detail": "Incorrect file format. Only jpgs, png, jpegs allowed"}
        imghex_name = await secrets.token_hex(10) + "." + extension
        return imghex_name

    async def get_promoted_products(self):
        pp = await self._session.execute(select(Product).where(Product.is_promoted))
        return pp.scalars().unique().all()

    async def get_active_products(self):
        pp = await self._session.execute(select(Product).where(Product.is_active))
        return pp.scalars().unique().all()

    async def list_vendor_products(self, user: Vendor):
        vproduct = await self._session.execute(select(Product).where(Product.vendor_id == user))
        return vproduct.scalars().unique().all()

 # ////////////////////  Add a product ///////////////////////////////

    async def create_product(self, product_data: dict, user: Vendor, files: Optional[list[UploadFile]], image_service: ImageOssServiceInterface,
                             ):
        imageUrl = []
        imageName = []
        FILEPATH = "product-images/"
        if files:
            for file in files:

                my_images_url = f'{uuid.uuid4()}-{file.filename}'
                object_name = FILEPATH + my_images_url
                await image_service.put_file(filename=object_name, raw_contents=file.file)
                imageUrl.append(
                    "https://afia4.oss-cn-beijing.aliyuncs.com/product-images/" + my_images_url[0:])
                imageName.append(my_images_url[0:])
                print(imageName)
                print(imageUrl)
        result = await self._session.execute(insert(Product).values(**product_data, vendor_id=user.id, imgs_url=imageUrl, imgs_name=imageName).returning(Product.id))
        product_id = result.scalars().first()
        await self._session.commit()
        product_result = await self._session.execute(select(Product).where(Product.id == product_id))
        return product_result.scalars().first()

 # ////////////////////  Add a product ///////////////////////////////

 # ////////////////////  Update product ///////////////////////////////

    async def update_product(self, product_id: int, updated_data: dict, user: Vendor,
                             ):
        if (product := await self._get_product(product_id=product_id)) and product.vendor_id != user.id:
            return False, None
        print(updated_data)
        _ = await self._session.execute(update(Product)
                                        .where(Product.id == product.id)
                                        .values(**updated_data)
                                        .returning(Product))
        await self._session.commit()
        await self._session.refresh(product)
        return True, product

 # ////////////////////  Update product ///////////////////////////////

 # ////////////////////  Deleting a product ///////////////////////////////

    async def _get_product_del(self, product_id: int, user) -> Product:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        if not (product := result.scalars().first()):
            raise HTTPException(detail='Product not found',
                                status_code=status.HTTP_404_NOT_FOUND)
        return product

    async def delete_product(self, product_id: int, user: Vendor, image_service: ImageOssServiceInterface):
        delProduct = await self._get_product_del(product_id=product_id, user=user)
        if delProduct.vendor_id != user.id:
            print(delProduct.owner_id, user.id, user.is_active)
            raise HTTPException(detail='You cannot delete this product',
                                status_code=status.HTTP_400_BAD_REQUEST)
        imageList = []
        images2del = delProduct.imgs_name
        if images2del:
            for url_img in images2del:
                imageList.append("product-images/" + url_img)
                await image_service.del_multiple_images(key_list=imageList)
                print(imageList)
        await self._session.delete(delProduct)
        await self._session.commit()

 # ////////////////////  Deleting a product ///////////////////////////////

    # async def get_favorite_products(self, offset: int, limit: int, user: User):
    #     result = await self._session.execute(select(Product)
    #                                          .join(Favorite)
    #                                          .where(Favorite.user_id == user.id, Favorite.is_favorite).offset(offset).limit(limit)
    #                                          .order_by(Product.updated.desc()))
    #     products: list[Product] = result.scalars().unique().all()
    #     return FavoriteSchema(user_id=user.id, products=products)

    # async def add_product_to_favorites(self, product_id: int, user: User):
    #     product = await self._get_product(product_id=product_id)
    #     result = await self._session.execute(insert(Favorite)
    #                                          .values(product_id=product.id, user_id=user.id, is_favorite=True)
    #                                          .returning(Favorite.id))
    #     await self._session.commit()
    #     if not result.is_insert:
    #         return False
    #     return True

    # async def remove_product_from_favorites(self, favorite_id: int, user: User):
    #     result = await self._session.execute(select(Favorite).where(Favorite.id == favorite_id, Favorite.user_id == user.id))
    #     if not (fav := result.scalars().first()):
    #         raise HTTPException(detail='Favorite products not found', status_code=status.HTTP_404_NOT_FOUND)
    #     await self._session.delete(fav)
    #     await self._session.commit()

    # async def _save_image(self, files: Optional[list[UploadFile]], image_service: ImageOssServiceInterface):
    #     imageUrl = []
    #     imageName = []
    #     FILEPATH = "product-images/"
    #     if files:
    #         for file in files:

    #             my_images_url = f'{uuid.uuid4()}-{file.filename}'
    #             object_name = FILEPATH + my_images_url
    #             await image_service.put_file(filename=object_name, raw_contents=file.file)
    #             imageUrl.append("https://afia4.oss-cn-beijing.aliyuncs.com/product-images/" + my_images_url[0:])
    #             imageName.append(my_images_url[0:])
    #             print(imageName)
    #             print(imageUrl)
    #             await self._session.execute(insert(Product).values(imgs_url=imageUrl, imgs_name=imageName))

    # async def create_product(self, product_data: dict, user: Vendor, files: Optional[list[UploadFile]], image_service: ImageOssServiceInterface,
    #                          ):
    #     result = await self._session.execute(insert(Product).values(**product_data, vendor_id=user.id).returning(Product.id))
    #     product_id = result.scalars().first()
    #     await self._save_image(files=files, image_service=image_service)
    #     await self._session.commit()
    #     product_result = await self._session.execute(select(Product).where(Product.id == product_id))
    #     return product_result.scalars().first()
