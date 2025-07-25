from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from webapp.schema.account.transaction import TransactionRead


class AccountCreate(BaseModel):
    account_name: str = Field(..., example='Main Wallet')


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None


class AccountRead(AccountCreate):
    account_id: int
    account_date: datetime
    transactions: list[TransactionRead] = []


class AccountsReadShort(AccountCreate):
    account_id: int
    account_name: str
    balance: float = 0.0
