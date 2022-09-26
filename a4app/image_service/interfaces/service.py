from abc import ABC, abstractmethod

from fastapi import UploadFile


class ImageOssServiceInterface(ABC):

    @abstractmethod
    async def put_file(self, filename=None, raw_contents=UploadFile):...


    @abstractmethod
    async def del_multiple_images(self, key_list=None):...