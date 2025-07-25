from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.billing.account import Account
from webapp.schema.account.account import AccountCreate


async def get_accounts_by_user_id(session: AsyncSession, user_id: int) -> List[Account]:
    stmt = select(Account).options(selectinload(Account.transactions)).where(Account.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_account_by_id(session: AsyncSession, account_id: int, user_id) -> Account | None:
    stmt = (
        select(Account)
        .options(selectinload(Account.transactions))
        .where(Account.account_id == account_id and Account.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_account(session: AsyncSession, account_data: AccountCreate, user_id: int) -> Account:
    account = Account(
        account_name=account_data.account_name,
        user_id=user_id,
    )
    session.add(account)
    try:
        await session.commit()
        new_account = await get_account_by_id(session, account.account_id, user_id)
        return new_account
    except Exception as e:
        await session.rollback()
        raise ValueError(f'Error creating account: {str(e)}')
