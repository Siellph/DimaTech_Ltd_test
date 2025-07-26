from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.billing.account import Account
from webapp.models.billing.transaction import Transaction


async def get_transactions_by_user_id(session: AsyncSession, user_id: int) -> List[Transaction]:
    stmt = select(Transaction).where(Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_transactions_by_account_id(session: AsyncSession, account_id: int, user_id: int) -> List[Transaction]:
    stmt = select(Transaction).where(Transaction.account_id == account_id and Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_transaction(session: AsyncSession, transaction_data: dict) -> Transaction:
    stmt = select(Account).where(
        Account.account_id == transaction_data['account_id'], Account.user_id == transaction_data['user_id']
    )
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()

    if account is None:
        account = Account(account_id=transaction_data['account_id'], user_id=transaction_data['user_id'], balance=0)
        session.add(account)
        await session.flush()

    transaction = Transaction(
        transaction_id=transaction_data['transaction_id'],
        account_id=transaction_data['account_id'],
        user_id=transaction_data['user_id'],
        amount=transaction_data['amount'],
        signature=transaction_data['signature'],
    )
    try:
        session.add(transaction)

        # Add transaction amount to account balance
        account.balance += transaction_data['amount']

        await session.commit()
        await session.refresh(transaction)
    except IntegrityError as e:
        await session.rollback()
        err_msg = str(e.orig)
        if 'uq_transaction_transaction_id' in err_msg:
            raise ValueError('Transaction with this ID already exists')
    return transaction
