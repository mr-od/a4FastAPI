from tkinter import Image
from typing import Optional
from a4app.products.models import Product
from a4app.users.models import User
from a4app.vendors.models import Vendor
from .interfaces.repositories_interface import OrderRepositoryInterface
from .models import PlacedOrder, OrderProduct, Address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .schemas import A4OrderSchema, OrderPAbstract, OrderPSchema, PlaceAssOrderSchema, PlacedOrderSchema, OrderProductSchema
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status


class OrderRepository(OrderRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_order(self, user: User):
        result = await self._session.execute(select(PlacedOrder).options(joinedload(PlacedOrder.order_products).joinedload(OrderProduct.product)).where(PlacedOrder.customer_id == user.id, PlacedOrder.is_paid == False))
        if not (_order := result.scalars().first()):
            return None
        return _order

    async def _get_order_or_none(self, user: User):
        _order: PlacedOrder = await self._get_order(user=user)
        if not _order:
            raise HTTPException(detail='Placed Order not found',
                                status_code=status.HTTP_404_NOT_FOUND)
        return _order

    async def get_order_products(self, user: User):
        _order = await self._get_order_or_none(user=user)
        products = [OrderPAbstract(
            id=p.id,
            product_id=p.product_id,
            quantity=p.quantity,
            vendor_id=p.vendor_id,
            order_id=p.order_id
        ) for p in _order.order_products]
        return PlacedOrderSchema(id=_order.id,
                                 customer_id=_order.customer_id,
                                 created=_order.created,
                                 completed=_order.completed,
                                 is_shipped=_order.is_shipped,
                                 is_closed=_order.is_closed,
                                 is_paid=_order.is_paid,
                                 is_cancelled=_order.is_canceled,
                                 delivery_fee=_order.delivery_fee,
                                 total=_order.total,
                                 subtotal=_order.subtotal,
                                 order_products=products
                                 )

    async def list_vendor_orders(self, user: Vendor):
        vorders = await self._session.execute(select(OrderProduct).where(OrderProduct.vendor_id == user))
        return vorders.scalars().unique().all()

    async def list_user_orders(self, user: User):
        uorders = await self._session.execute(select(PlacedOrder).where(PlacedOrder.customer_id == user))
        return uorders.scalars().unique().all()

    async def get_completed_order_products(self, user: User):
        _order = await self._get_order_or_none(user=user)
        total_price = _order.get_total_price
        products = [OrderProductSchema(
            product=p.product, quantity=p.quantity, id=p.id, order_id=p.order_id) for p in _order.order_products]
        return PlacedOrderSchema(id=_order.id, customer_id=_order.customer_id, completed=_order.created, is_completed=_order.is_completed,
                                 order_products=products, total_price=total_price)

    async def get_shipped_order_products(self, user: User):
        _order = await self._get_order_or_none(user=user)
        total_price = _order.get_total_price
        products = [OrderProductSchema(
            product=p.product, quantity=p.quantity, id=p.id, order_id=p.order_id) for p in _order.order_products]
        return PlacedOrderSchema(id=_order.id, customer_id=_order.customer_id, completed=_order.created, is_completed=_order.is_shipped,
                                 order_products=products, total_price=total_price)

    async def remove_order(self, order_product_id: int, user: User):
        _order = await self._get_order_or_none(user=user)
        order_product_result = await self._session.execute(select(OrderProduct)
                                                           .where(OrderProduct.id == order_product_id, OrderProduct.order_id == _order.id))
        _order_product = order_product_result.scalars().first()
        if not _order_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Order Product not found')
        if _order_product.quantity > 1:
            _order_product.quantity -= 1
            await self._session.commit()
        else:
            await self._session.delete(_order_product)
            await self._session.commit()

    async def add_shipping_address_and_payment(self, shipping_address: dict, user: User):
        _order: PlacedOrder = await self._get_order_or_none(user=user)
        result = await self._session.execute(insert(Address).values(**shipping_address).returning(Address.id))
        await self._session.commit()
        shipping_address_id = result.scalar()
        _order.shipping_address = shipping_address_id

        # --> add payment system <--

        _order.is_ordered = True
        await self._session.commit()

    async def _get_product(self, product_id: int) -> Product:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        if not (product := result.scalars().first()):
            raise HTTPException(detail='Product not found',
                                status_code=status.HTTP_404_NOT_FOUND)
        return product

    async def _order_id_product(self, order_id: int, aos: list[dict]):
        res = []
        if aos:
            for a in aos:
                product_res = await self._session.execute(select(Product).where(Product.id == a.product_id))
                product = product_res.scalars().first()
                order_product_result = await self._session.execute(insert(OrderProduct)
                                                                   .values(order_id=order_id, product_id=a.product_id, vendor_id=product.vendor_id, quantity=a.quantity).returning(OrderProduct))
                final_result = order_product_result.first()
                res.append(final_result[0:])
                await self._session.commit()

    async def order_id_product(self, order_id: int, aos: list[dict]):
        # SuperUser Add Product(s) to Order
        res = []
        if aos:
            for a in aos:
                product_res = await self._session.execute(select(Product).where(Product.id == a.product_id))
                product = product_res.scalars().first()
                order_product_result = await self._session.execute(insert(OrderProduct)
                                                                   .values(order_id=order_id, product_id=a.product_id, vendor_id=product.vendor_id, quantity=a.quantity).returning(OrderProduct))
                final_result = order_product_result.first()
                res.append(final_result)
                await self._session.commit()
        return res

    async def place_an_order(self, order_details: dict, productQuantity: list[dict], user: User):
        result = await self._session.execute(insert(PlacedOrder).values(**order_details, customer_id=user.id, is_paid=True).returning(PlacedOrder.id))
        placed_order_id = result.scalars().first()
        await self._order_id_product(order_id=placed_order_id, aos=productQuantity)
        await self._session.commit()
        placed_order_result = await self._session.execute(select(PlacedOrder).where(PlacedOrder.id == placed_order_id))
        return placed_order_result.scalars().first()
