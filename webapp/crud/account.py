from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.billing.account import Account
from webapp.schema.account.account import AccountUpdate


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


async def update_account(session: AsyncSession, account_id: int, account_data: AccountUpdate, user_id: int) -> Account:
    account = await get_account_by_id(session, account_id, user_id)
    if not account:
        raise ValueError('Account not found or does not belong to the user')

    if account_data.account_name is not None:
        account.account_name = account_data.account_name

    try:
        await session.commit()
        await session.refresh(account)
    except IntegrityError as e:
        await session.rollback()
        err_msg = str(e.orig)
        if 'uq_account_account_name' in err_msg:
            raise ValueError('Account with this name already exists for the user')
        raise ValueError(f'Error updating account: {str(e)}')

    return account
