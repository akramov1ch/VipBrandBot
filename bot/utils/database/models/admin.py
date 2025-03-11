from sqlalchemy import Column, String, BigInteger
from bot.utils.database.models.base import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(BigInteger, primary_key=True, index=True)
    tg_id = Column(BigInteger, index=True, unique=True, nullable=False)

    full_name = Column(String, nullable=False)
