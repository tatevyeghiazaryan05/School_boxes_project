from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, text,ARRAY, Boolean
from database import Base


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, nullable=False, primary_key=True)
    product_brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    color = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, server_default="0")
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=False)
    discount = Column(Float, server_default="0.0")
    tags = Column(ARRAY(String), nullable=False)
