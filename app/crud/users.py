from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.models import User
from core.schemas.users import UserCreate
from crud.base import BaseCRUD


class UserCRUD(BaseCRUD):
    model = User

    @classmethod
    async def get_all_users(
            cls,
            session: AsyncSession,
    ) -> Sequence[User]:
        # Statement
        stmt = select(cls.model).order_by(cls.model.id)
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    async def create_user(
            cls,
            session: AsyncSession,
            user_create: UserCreate,
    ) -> User:
        user = User(**user_create.model_dump())
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise e