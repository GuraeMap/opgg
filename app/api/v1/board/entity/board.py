from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.api.v1.user.entity.user
from app.api.v1.user.entity.user import User
from app.config.db.time_stamp_mixin import TimeStampMixin


class Board(TimeStampMixin):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    contents: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    view_count: Mapped[int] = mapped_column(Integer)

    user = relationship(app.api.v1.user.entity.user.User)
