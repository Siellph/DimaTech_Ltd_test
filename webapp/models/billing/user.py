from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[str] = mapped_column(String, default='user')
    full_name: Mapped[str] = mapped_column(String)

    accounts = relationship(
        'Account',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    transactions = relationship(
        'Transaction',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
