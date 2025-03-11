import datetime
from sqlalchemy import Column, String, DateTime, BigInteger
from bot.utils.database.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    tg_id = Column(BigInteger, index=True, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    language = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
