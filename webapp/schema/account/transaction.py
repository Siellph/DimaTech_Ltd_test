from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    transaction_id: UUID = Field(..., example='5eae174f-7cd0-472c-bd36-35660f00132b')
    account_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    amount: Decimal = Field(..., example='100')
    signature: str = Field(..., example='7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8')


class TransactionRead(TransactionCreate):
    id: int
    timestamp: datetime
    signature: str
