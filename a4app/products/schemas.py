from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Form, Query


class CreateOrUpdateProductSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    price: Optional[float] = Field(None, gt=0.0)
    color: Optional[str]
    gender: Optional[str]
    brand: Optional[str]
    material: Optional[str]
    memory_size: Optional[str]
    screen_size: Optional[str]
    condition: Optional[str]

    @classmethod
    def as_form(cls,
                name: Optional[str] = Form(None),
                description: Optional[str] = Form(None),
                price: Optional[float] = Form(None),
                color: Optional[str] = Form(None),
                gender: Optional[str] = Form(None),
                brand: Optional[str] = Form(None),
                material: Optional[str] = Form(None),
                ):
        return cls(name=name, description=description, price=price, color=color, gender=gender, brand=brand, material=material)


class ProductSchema(CreateOrUpdateProductSchema):
    id: int
    created: datetime
    updated: datetime
    is_active: bool = True
    is_promoted: bool = False
    vendor_id: Optional[int] = None
    imgs_url: Optional[list[str]]
    imgs_name: Optional[list[str]]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}


class GadgetSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    price: Optional[float] = Field(None, gt=0.0)
    color: Optional[str]
    size: Optional[str]
    brand: Optional[str]
    memory_size: Optional[str]
    screen_size: Optional[str]
    condition: Optional[str]

    @classmethod
    def as_form(cls,
                name: Optional[str] = Form(None),
                description: Optional[str] = Form(None),
                price: Optional[float] = Form(None),
                color: Optional[str] = Form(None),
                memory_size: Optional[str] = Form(None),
                screen_size: Optional[str] = Form(None),
                brand: Optional[str] = Form(None),
                condition: Optional[str] = Form(None),
                ):
        return cls(name=name, description=description, price=price, color=color, memory_size=memory_size, screen_size=screen_size, brand=brand, condition=condition)


class GadgetRSchema(GadgetSchema):
    id: int
    created: datetime
    updated: datetime
    is_active: bool = True
    is_promoted: bool = False
    vendor_id: Optional[int] = None
    imgs_url: Optional[list[str]]
    imgs_name: Optional[list[str]]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}
