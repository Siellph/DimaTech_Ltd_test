from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.billing.transaction import Transaction


async def get_transactions_by_user_id(session: AsyncSession, user_id: int) -> List[Transaction]:
    stmt = select(Transaction).where(Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_transactions_by_account_id(session: AsyncSession, account_id: int, user_id: int) -> List[Transaction]:
    stmt = select(Transaction).where(Transaction.account_id == account_id and Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
