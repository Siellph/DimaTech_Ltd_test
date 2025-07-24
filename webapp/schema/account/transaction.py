from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: Decimal = Field(..., example='100.00')
    status: str


class TransactionUpdate(BaseModel):
    status: Optional[str] = None
    signature: Optional[str] = None


class TransactionRead(TransactionCreate):
    id: int
    timestamp: datetime
    signature: str
