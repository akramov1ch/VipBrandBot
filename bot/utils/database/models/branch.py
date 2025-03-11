from sqlalchemy import Column, String, Float, Boolean, Integer
from bot.utils.database.models.base import Base

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    branch_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
    address = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    phone = Column(String, nullable=False)
    opening_hours = Column(String, nullable=False)
    closing_hours = Column(String, nullable=False)
    instagram_have = Column(Boolean, nullable=False)
    instagram_link = Column(String, nullable=False, default="")