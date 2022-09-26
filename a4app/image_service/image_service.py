from __future__ import print_function
import sys
import logging
import oss2
import oss2.exceptions
from pathlib import Path
from fastapi import UploadFile
from .interfaces.service import ImageOssServiceInterface
from core.config import get_settings



logger = logging.getLogger("fastapi_oss")

class ImageOssService(ImageOssServiceInterface):

    def __init__(self,
    #  path: str = None,
     ossApp=None,
     files: list = None,
     filename: str = None,
     images_list: str = None
     ) -> None:
        # self._path = path,
        self._files = files
        if ossApp is not None:
            self.init_app(ossApp)

    _access_key = get_settings().oss_access_key_id
    _secret = get_settings().oss_secret_access_key
    _endpoint = get_settings().oss_endpoint
    _bucket_name = get_settings().bucket_name
    auth = oss2.Auth(_access_key, _secret)
    bucket = oss2.Bucket(auth, _endpoint, _bucket_name)

    # async def read_image(self, imagename: str, **kwargs):
    #     try:
    #         async with aiofiles.open(f'{self._path}/{imagename}', mode='rb') as file:
    #             image = await file.read()
    #         return image
    #     except FileNotFoundError as error:
    #         raise FileNotFoundError(error)


    async def put_file(self, filename=str, raw_contents=UploadFile):

        success = self.bucket.put_object(filename, raw_contents)
        if success.status == 200:
            return filename
        else:
            logger.error(f"FAILURE writing file(s) {filename}")


    async def del_multiple_images(self, key_list=None):
        is_delete = False
        try:
            self.bucket.batch_delete_objects(key_list)
            print(key_list)
            is_delete = True
        except oss2.exceptions.NoSuchKey as e:
            logger.error(
                f"{key_list} not found: http_status={e.status}, request_id={e.request_id}"
            )
        return is_delete


    # async def write_image(self, imagename: str, image: UploadFile, **kwargs):
    #     async with aiofiles.open(f'{self._path}/{imagename}', mode='wb') as file:
    #         content = await image.read()
    #         await file.write(content)

    # async def delete_image(self, imagename: str, **kwargs):
    #     try:
    #         await _os.remove(f'{self._path}/{imagename}')
    #     except FileNotFoundError as error:
    #         raise FileNotFoundError(error)

        