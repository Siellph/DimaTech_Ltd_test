from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.billing.account import Account
from webapp.models.billing.user import User
from webapp.schema.login.user import UserCreate
from webapp.utils.auth.password import hash_password


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    stmt = (
        select(User)
        .options(selectinload(User.accounts).selectinload(Account.transactions))
        .where(User.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    stmt = (
        select(User)
        .options(selectinload(User.accounts).selectinload(Account.transactions))
        .where(User.username == username)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> List[User]:
    stmt = select(User).options(selectinload(User.accounts).selectinload(Account.transactions))
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
    )
    session.add(user)
    try:
        await session.commit()

        # Повторная загрузка с подгрузкой связанных accounts
        result = await session.execute(
            select(User)
            .options(selectinload(User.accounts).selectinload(Account.transactions))
            .where(User.user_id == user.user_id)
        )
        user_with_accounts = result.scalar_one()

        return user_with_accounts
    except Exception as e:
        await session.rollback()
        error_msg = str(e.orig)
        if 'uq_user_username' in error_msg:
            raise ValueError('Пользователь с таким username уже существует')
        elif 'uq_user_email' in error_msg:
            raise ValueError('Пользователь с таким email уже существует')
        else:
            raise ValueError('Ошибка при создании пользователя: ' + str(e))


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True
