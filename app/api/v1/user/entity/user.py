from sqlalchemy import BigInteger, String, Boolean

from app.config.db.time_stamp_mixin import TimeStampMixin
from sqlalchemy.orm import mapped_column, Mapped


class User(TimeStampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_session: Mapped[bool] = mapped_column(Boolean, default=0, doc ="1 : 회원 탈퇴 ")
