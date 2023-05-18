from typing import Optional, Union

from timetable import db
from timetable.models.user import User


def get_user(user_id: Union[int, str]) -> Optional[User]:
    return db.session.query(User).get(user_id)


def get_by_username(username: str) -> Optional[User]:
    return db.session.query(User).filter_by(username=username).first()
