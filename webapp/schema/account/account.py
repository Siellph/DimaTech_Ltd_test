from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from webapp.schema.account.transaction import TransactionRead


class AccountCreate(BaseModel):
    account_name: str = Field(..., example='Main Wallet')
    user_id: int
    balance: float = 0.0


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    balance: Optional[float] = None


class AccountRead(AccountCreate):
    account_id: int
    account_date: datetime
    transactions: list[TransactionRead] = []
