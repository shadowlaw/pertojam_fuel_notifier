from sqlalchemy import Column, String

from config import Base


class FuelCategory(Base):
    __tablename__ = "fuel_category"

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
