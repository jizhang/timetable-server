from typing import Optional, Union

from sqlalchemy import select

from timetable import db
from timetable.models.user import User


def get_user(user_id: Union[int, str]) -> Optional[User]:
    return db.session.get(User, user_id)


def get_by_username(username: str) -> Optional[User]:
    return db.session.scalar(
        select(User)
        .filter_by(username=username),
    )
