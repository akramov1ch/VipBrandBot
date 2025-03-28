import datetime
import os
from typing import Sequence

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from bot.utils.database.models.base import Base
from bot.utils.logger import logger

from bot.utils.database.models.admin import Admin
from bot.utils.database.models.user import User
from bot.utils.database.models.branch import Branch

from bot.types import admin as admin_types
from bot.types import user as user_types
from bot.types import branch as branch_types

db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Cruds:
    @staticmethod
    async def create_admin(admin: admin_types.AdminCreate) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    new_obj = Admin(**admin.model_dump())
                    session.add(new_obj)
                return True
        except:
            logger.exception("Database exception")
            return False

    @staticmethod
    async def delete_admin(tg_id: int) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(Admin).filter(Admin.tg_id.__eq__(tg_id))
                    result = await session.execute(query)
                    admin_instance = result.scalars().first()
                    if not admin_instance:
                        return False
                    await session.delete(admin_instance)
                return True
        except:
            logger.exception("Database exception")
            return False

    @staticmethod
    async def get_admins() -> Sequence[Admin] | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(Admin)
                    result = await session.execute(query)
                    return result.scalars().all()
        except:
            logger.exception("Database exception")
            return None

    @staticmethod
    async def get_admin(tg_id: int = None) -> Admin | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(Admin)
                    if tg_id is not None:
                        query = query.filter(Admin.tg_id.__eq__(tg_id))
                    result = await session.execute(query)
                    return result.scalars().first()
        except:
            logger.exception("Database exception")
            return None

    @staticmethod
    async def create_user(user: user_types.UserCreate) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    new_obj = User(**user.model_dump())
                    session.add(new_obj)
                return True
        except:
            logger.exception("Database exception")
            return False

    @staticmethod
    async def update_language(*, tg_id: int, language: str) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(User).filter(User.tg_id.__eq__(tg_id))
                    result = await session.execute(query)
                    _instance = result.scalars().first()
                    if not _instance:
                        return False
                    setattr(_instance, "language", language)
                return True
        except:
            logger.exception("Database exception")
            return False

    @staticmethod
    async def get_users() -> Sequence[User] | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(User)
                    result = await session.execute(query)
                    return result.scalars().all()
        except:
            logger.exception("Database exception")
            return None

    @staticmethod
    async def get_user(tg_id: int = None) -> User | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(User)
                    if tg_id is not None:
                        query = query.filter(User.tg_id.__eq__(tg_id))
                    result = await session.execute(query)
                    return result.scalars().first()
        except:
            logger.exception("Database exception")
            return None

    @staticmethod
    async def count_users_today() -> int | None:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                today = datetime.datetime.utcnow().date()
                start_date = datetime.datetime(today.year, today.month, today.day)
                query = select(func.count()).select_from(User).filter(User.created_at >= start_date)
                result = await session.execute(query)
                return result.scalars().first()

    @staticmethod
    async def count_users_this_week() -> int | None:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                today = datetime.datetime.utcnow()
                start_date = today - datetime.timedelta(days=today.weekday())
                query = select(func.count()).select_from(User).filter(User.created_at >= start_date)
                result = await session.execute(query)
                return result.scalars().first()

    @staticmethod
    async def count_users_this_month() -> int | None:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                today = datetime.datetime.utcnow()
                start_date = datetime.datetime(today.year, today.month, 1)
                query = select(func.count()).select_from(User).filter(User.created_at >= start_date)
                result = await session.execute(query)
                return result.scalars().first()

    @staticmethod
    async def count_users_total() -> int | None:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                query = select(func.count()).select_from(User)
                result = await session.execute(query)
                return result.scalars().first()

    @staticmethod
    async def get_branches_by_type(branch_type: str) -> Sequence[Branch] | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(Branch).filter(Branch.branch_type == branch_type)
                    result = await session.execute(query)
                    return result.scalars().all()
        except:
            logger.exception("Database exception")
            return None

    @staticmethod
    async def create_branch(branch: branch_types.BranchCreate) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    branch_data = branch.model_dump()
                    # instagram_link None bo‘lsa, bo‘sh qatorga o‘zgartirish
                    if branch_data["instagram_link"] is None:
                        branch_data["instagram_link"] = ""
                    logger.info(f"Creating branch with data: {branch_data}")
                    new_obj = Branch(**branch_data)
                    session.add(new_obj)
                    await session.commit()
                logger.info("Branch successfully created")
                return True
        except Exception as e:
            logger.exception(f"Database exception occurred: {str(e)}")
            return False
        
    @staticmethod
    async def get_branch_by_id(branch_id: int) -> Branch | None:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = select(Branch).filter(Branch.id == branch_id)
                    result = await session.execute(query)
                    return result.scalars().first()
        except:
            logger.exception("Database exception")
            return None
        
    @staticmethod
    async def delete_branch(branch_id: int) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    query = delete( Branch).where(Branch.id == branch_id)
                    result = await session.execute(query)
                    await session.commit()
                    return result.rowcount > 0  # Agar o‘chirilgan bo‘lsa True qaytaradi
        except Exception as e:
            logger.exception(f"Error in delete_branch: {str(e)}")
            return False
