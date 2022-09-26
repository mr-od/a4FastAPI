from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from a4app.products.schemas import GadgetSchema, ProductSchema


class CreateAddressSchema(BaseModel):
    country: Optional[str]
    city: str
    street: Optional[str]
    house_number: Optional[str]
    apartment_number: Optional[str]
    zipcode: Optional[str]


class AddressSchema(CreateAddressSchema):
    id: int
    user_id: int


class OrderProductSchema(BaseModel):
    id: int
    order_id: int
    quantity: int = 1
    products: GadgetSchema | None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}


class OrderPSchema(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderPAbstract(OrderPSchema):
    order_id: int
    vendor_id: int

    class Config:
        orm_mode = True


class A4OrderSchema(BaseModel):
    total: float | None
    subtotal: float | None
    delivery_fee: float | None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}


class PlacedOrderSchema(BaseModel):
    id: int
    customer_id: int
    created: datetime
    completed: datetime | None
    is_paid: bool | None
    is_closed: bool | None
    is_shipped: bool | None
    is_cancelled: bool | None
    total: float | None
    subtotal: float | None
    delivery_fee: float | None
    order_products: list[OrderPAbstract]
    # shipping_address: Optional[AddressSchema]


class PlaceAnOrderSchema(BaseModel):

    subtotal: Optional[float] = Field(None, gt=0.0)
    delivery_fee: Optional[float] = Field(None, gt=0.0)
    total: Optional[float] = Field(None, gt=0.0)
    order_products: list[OrderPSchema]

    @classmethod
    def as_form(cls,
                order_products: Optional[list[OrderPSchema]],
                subtotal: Optional[float] = Form(None),
                delivery_fee: Optional[float] = Form(None),
                total: Optional[float] = Form(None),
                ):
        return cls(subtotal=subtotal, delivery_fee=delivery_fee, total=total, order_products=order_products
                   )


class PlaceAssOrderSchema(BaseModel):

    subtotal: Optional[float] = Field(None, gt=0.0)
    delivery_fee: Optional[float] = Field(None, gt=0.0)
    total: Optional[float] = Field(None, gt=0.0)

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}


class FinalOrderSchema(BaseModel):

    subtotal: Optional[float] = Field(None, gt=0.0)
    delivery_fee: Optional[float] = Field(None, gt=0.0)
    total: Optional[float] = Field(None, gt=0.0)
    order_products: list[OrderPSchema]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')}
