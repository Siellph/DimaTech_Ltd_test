from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.billing.account import Account
from webapp.models.billing.user import User
from webapp.schema.login.user import UserCreate, UserUpdate
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

        user_with_accounts = await get_user_by_id(session, user.user_id)

        return user_with_accounts
    except Exception as e:
        await session.rollback()
        error_msg = str(e.orig)
        if 'uq_user_username' in error_msg:
            raise ValueError('A user with this username already exists')
        elif 'uq_user_email' in error_msg:
            raise ValueError('A user with this email already exists')
        else:
            raise ValueError('Error creating user: ' + str(e))


async def update_user(session: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
    user = await get_user_by_id(session, user_id)
    if not user:
        raise ValueError('User not found')

    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email
    if user_data.full_name:
        user.full_name = user_data.full_name
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)

    session.add(user)
    try:
        await session.commit()
        user_with_accounts = await get_user_by_id(session, user.user_id)
        return user_with_accounts
    except Exception as e:
        await session.rollback()
        error_msg = str(e.orig)
        if 'uq_user_username' in error_msg:
            raise ValueError('The username is occupied')
        elif 'uq_user_email' in error_msg:
            raise ValueError('The email is occupied')
        else:
            raise ValueError('Update error: ' + str(e))


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True
