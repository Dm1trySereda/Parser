from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(book_num={self.book_num},"
            f" title={self.title},"
            f"author={self.author},"
            f" price_new={self.price_new}, price_old={self.price_old},"
            f" discount={self.discount}, rating={self.rating},"
            f" image={self.image})"
        )
