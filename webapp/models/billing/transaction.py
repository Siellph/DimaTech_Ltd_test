import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey(f'{DEFAULT_SCHEMA}.account.account_id', ondelete='CASCADE'),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(f'{DEFAULT_SCHEMA}.user.user_id', ondelete='CASCADE'), nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    signature: Mapped[str] = mapped_column(String, nullable=False)

    account = relationship('Account', back_populates='transactions')
    user = relationship('User', back_populates='transactions')
