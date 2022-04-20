from sqlalchemy import Column, Integer, String, ForeignKey, Float, func, Date

from config import Base


class PriceChange(Base):
    __tablename__ = "price_change"

    id = Column(Integer, primary_key=True)
    fuel_category_id = Column(String(10), ForeignKey("fuel_category.id"), nullable=False)
    date = Column(Date, nullable=False, server_default=func.now())
    current_price = Column(Float, nullable=False)
    price_change = Column(Float, nullable=False)
    percentage_change = Column(Float, nullable=False)
