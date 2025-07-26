from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from webapp.schema.account.transaction import TransactionRead


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None


class AccountRead(AccountUpdate):
    account_id: int
    account_date: datetime
    balance: float
    transactions: list[TransactionRead] = []


class AccountsReadShort(AccountUpdate):
    account_id: int
    balance: float
