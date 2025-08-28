from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.users import UserRead, UserCreate
from crud.users import UserCRUD

router = APIRouter(tags=["Users",])


@router.get("", summary="Получить всех пользователей", response_model=list[UserRead])
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await UserCRUD.get_all_users(session=session)
    return users


@router.post("", summary="Создать пользователя", response_model=UserRead)
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: UserCreate,
):
    result_user = await UserCRUD.create_user(
        session=session,
        user_create=user
    )
    return result_user
