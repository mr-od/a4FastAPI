from core.database import Base
import sqlalchemy as _sql
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM


class Product(Base):
    __tablename__ = 'products'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String(length=255), nullable=False)
    description = _sql.Column(_sql.String, nullable=True)
    price = _sql.Column(_sql.Numeric(12, 2))
    color = _sql.Column(_sql.String, nullable=True)
    gender = _sql.Column(_sql.String, nullable=True)
    brand = _sql.Column(_sql.String, nullable=True)
    material = _sql.Column(_sql.String, nullable=True)
    size = _sql.Column(_sql.String, nullable=True)
    memory_size = _sql.Column(_sql.String, nullable=True)
    screen_size = _sql.Column(_sql.String, nullable=True)
    condition = _sql.Column(_sql.String, nullable=True)

    created = _sql.Column(_sql.DateTime, default=datetime.now)
    updated = _sql.Column(
        _sql.DateTime, default=datetime.now, onupdate=datetime.now)
    owner = relationship("Vendor", back_populates="product")
    imgs_url = _sql.Column(_sql.ARRAY(_sql.String), nullable=True)
    imgs_name = _sql.Column(_sql.ARRAY(_sql.String), nullable=True)

    is_active = _sql.Column(_sql.Boolean, default=True)
    is_promoted = _sql.Column(_sql.Boolean, default=False)
    # is_popular = _sql.Column(_sql.Boolean, default=False)

    # is_electronic = _sql.Column(_sql.Boolean, default=False)
    # is_fashion = _sql.Column(_sql.Boolean, default=False)
    # is_gadget = _sql.Column(_sql.Boolean, default=False)

    order_products = relationship(
        'OrderProduct', backref='product', cascade='all, delete', lazy='joined')
    vendor_id = _sql.Column(_sql.Integer, _sql.ForeignKey('vendors.id'))

    def __repr__(self) -> str:
        return f'Product: {self.title} {self.price}'
