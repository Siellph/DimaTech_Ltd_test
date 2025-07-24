import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Account(Base):
    __tablename__ = 'account'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    account_name: Mapped[str] = mapped_column(String, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f'{DEFAULT_SCHEMA}.user.user_id', ondelete='CASCADE'), nullable=False
    )
    account_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
    balance: Mapped[float] = mapped_column(default=0.0)

    user = relationship('User', back_populates='accounts')
    transactions = relationship(
        'Transaction', back_populates='account', cascade='all, delete-orphan', passive_deletes=True, lazy='selectin'
    )
