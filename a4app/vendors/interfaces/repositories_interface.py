from abc import ABC, abstractmethod
from typing import Optional
from ..models import Vendor


class AuthRepositoryInterface(ABC):
    @abstractmethod
    async def save_vendor(self, email: str, username: str, password: str, is_admin: bool = False): pass

    @abstractmethod
    async def get_vendor_by_email(self, email: str) -> Vendor: pass

    @abstractmethod
    async def get_vendor_by_username(self, username: str) -> Vendor: pass

class ProfileRepositoryInterface(ABC):

    @abstractmethod
    async def get_vendor(self, vendor: Vendor) -> Vendor: pass

    @abstractmethod
    async def update_vendor(self, vendor: Vendor, updated_data: dict): pass

    @abstractmethod
    async def delete_user(self, vendor: Vendor): pass
