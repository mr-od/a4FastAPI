from abc import ABC, abstractmethod

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordServiceInterface(ABC):
    @abstractmethod
    async def get_hashed_password(self, password: str): pass

    @abstractmethod
    async def   verify_password(self, plain_password: str, hashed_password: str) -> bool: pass


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
