from typing import List, Optional
from fastapi import APIRouter, Depends, status
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from a4app.users.permissions import GetUser
from a4app.users.models import User
from a4app.users.token_service import TokenService
from a4app.orders.services import OrderService
from a4app.orders.repositories import OrderRepository
from a4app.orders.schemas import OrderPAbstract, OrderPSchema, PlaceAnOrderSchema, PlaceAssOrderSchema, PlacedOrderSchema, CreateAddressSchema
from a4app.vendors.models import Vendor
from a4app.vendors.permissions import GetVendor


orders_routers = APIRouter()


@orders_routers.post('/payment')
async def add_shipping_address_and_fake_pay_order(shipping_address: CreateAddressSchema, db: AsyncSession = Depends(get_db),
                                                  user: User = Depends(GetUser(token_service=TokenService()))):
    return await OrderService(repository=OrderRepository(session=db)).payment_order(user=user, shipping_address=shipping_address)


@orders_routers.get('/', status_code=status.HTTP_200_OK, response_model=PlacedOrderSchema)
async def get_order(db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await OrderService(repository=OrderRepository(session=db)).get_order(user=user)


@orders_routers.delete('/{order_product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_order(order_product_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    await OrderService(repository=OrderRepository(session=db)).remove_order(user=user, order_product_id=order_product_id)
    return {'detail': 'Order has been removed'}


@orders_routers.post('/place/', status_code=status.HTTP_201_CREATED)
async def place_an_order(productQuantity: list[OrderPSchema], order_details: PlaceAssOrderSchema,
                         db: AsyncSession = Depends(get_db),  user: User = Depends(GetUser(token_service=TokenService()))
                         ):
    return await OrderService(repository=OrderRepository(session=db)) \
        .place_an_order(order_details=order_details, productQuantity=productQuantity, user=user)


@orders_routers.get("/vendor", status_code=status.HTTP_200_OK, response_model=list[OrderPAbstract])
async def read_vendor_orders(db: AsyncSession = Depends(get_db), current_user: Vendor = Depends(GetVendor(token_service=TokenService()))) -> dict:
    """
    See all Current Active Vendor Orders. This shows all the orders of the currently logged in Vendor.
    """
    return await OrderService(repository=OrderRepository(session=db)).list_vendor_orders(user=current_user.id)


@orders_routers.get("/user", status_code=status.HTTP_200_OK)
async def read_user_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(GetUser(token_service=TokenService()))) -> dict:
    """
    See all Current Active User Orders. This shows all the orders of the currently logged in Used.
    """
    return await OrderService(repository=OrderRepository(session=db)).list_user_orders(user=current_user.id)


@orders_routers.post('/place/{order_id}', status_code=status.HTTP_201_CREATED, response_model=list[OrderPAbstract])
async def aos(aos: list[OrderPSchema], order_id: int,
              db: AsyncSession = Depends(get_db),
              ):
    return await OrderService(repository=OrderRepository(session=db)) \
        .order_id_product(order_id=order_id, aos=aos)
