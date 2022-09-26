from abc import ABC, abstractmethod
from a4app.users.models import User
from a4app.vendors.models import Vendor


class OrderRepositoryInterface(ABC):

    @abstractmethod
    async def get_order_products(self, user: User): pass

    @abstractmethod
    async def get_completed_order_products(self, user: User): pass

    @abstractmethod
    async def get_shipped_order_products(self, user: User): pass

    @abstractmethod
    async def remove_order(self, order_product_id: int, user: User): pass

    @abstractmethod
    async def add_shipping_address_and_payment(
        self, shipping_address: dict, user: User): pass

    @abstractmethod
    async def place_an_order(self, order_details: dict,
                             productQuantity: list[dict], user: User): pass

    @abstractmethod
    async def list_vendor_orders(self, user: Vendor): pass

    @abstractmethod
    async def list_user_orders(self, user: User): pass

    @abstractmethod
    async def order_id_product(self, order_id: int, aos: list[dict]): pass
