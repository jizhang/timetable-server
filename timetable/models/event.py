from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    title: Mapped[str]
    category_id: Mapped[int]
    start: Mapped[datetime]
    end: Mapped[datetime]
    created: Mapped[datetime]
    updated: Mapped[datetime]
