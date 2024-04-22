import datetime

from pytz import timezone

from sqlalchemy import DateTime, DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db.database import Base


class TimeStampMixin(Base):
    __abstract__ = True
    created_at: Mapped[DateTime] = mapped_column(
        DATETIME,
        nullable=False,
        default=lambda: datetime.datetime.now(timezone("Asia/Seoul")),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DATETIME,
        nullable=False,
        default=lambda: datetime.datetime.now(timezone("Asia/Seoul")),
        onupdate=lambda: datetime.datetime.now(timezone("Asia/Seoul")),
    )
