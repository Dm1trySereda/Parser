from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(book_num={self.book_num},"
            f" title={self.title},"
            f"author={self.author},"
            f" price_new={self.price_new}, price_old={self.price_old},"
            f" discount={self.discount}, rating={self.rating},"
            f" image={self.image})"
        )
