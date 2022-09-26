from typing import List, Optional
from a4app.users.models import User
from a4app.vendors.models import Vendor
from .interfaces.repositories_interface import OrderRepositoryInterface
from .schemas import A4OrderSchema, CreateAddressSchema, OrderPSchema, PlaceAnOrderSchema, PlaceAssOrderSchema


class OrderService:
    def __init__(self, repository: OrderRepositoryInterface):
        self._repository = repository

    async def get_order(self, user: User):
        return await self._repository.get_order_products(user=user)

    async def add_order(self, user: User, product_id: int):
        return await self._repository.add_order(product_id=product_id, user=user)

    async def remove_order(self, user: User, order_product_id: int):
        return await self._repository.remove_order(order_product_id=order_product_id, user=user)

    async def payment_order(self, user: User, shipping_address: CreateAddressSchema):
        return await self._repository.add_shipping_address_and_payment(shipping_address=shipping_address.dict(exclude_none=True), user=user)

    async def place_an_order(self, order_details: PlaceAssOrderSchema, productQuantity: list[OrderPSchema], user: User):
        return await self._repository.place_an_order(user=user, productQuantity=productQuantity, order_details=order_details.dict(exclude_none=True))

    async def list_vendor_orders(self, user: Vendor):
        return await self._repository.list_vendor_orders(user=user)

    async def list_user_orders(self, user: User):
        return await self._repository.list_user_orders(user=user)

    async def order_id_product(self, order_id: int, aos: list[dict]):
        return await self._repository.order_id_product(order_id=order_id, aos=aos)
