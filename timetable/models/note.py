from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    content: Mapped[str]
    created: Mapped[datetime]
