import os
from fastapi import FastAPI
from mysql.connector import connect
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

db_connection = connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)


@app.get("/")
async def read_root():
    return {"hello from "}


# Пагинация
@app.get("/books/")
async def read_root(page: int = 1):
    books_limit = 10
    books_offset = (page - 1) * books_limit  # сколько книг пропускаем
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        "SELECT DISTINCT book_id, `date`,title,author,price,price_old,discount,rating FROM books ORDER BY title LIMIT %s OFFSET %s;",
        (books_limit, books_offset))
    result = db_cursor.fetchall()
    library = []
    for book in result:
        books_dict = {
            'book_id': book[0],
            'Дата': book[1],
            'Название книги': book[2],
            'Автор': book[3],
            'Новая цена': book[4],
            'Старая цена': book[5],
            'Скидка': book[6],
            'Рейтинг': book[7],
        }
        library.append(books_dict)
        db_cursor.close()
        db_connection.commit()
    return library


# Поиск книги
@app.get("/search")
async def search_books(name: str = None):
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "SELECT DISTINCT book_id, `date`,title,author,price,price_old,discount,rating FROM books WHERE title LIKE  %s",
        ('%' + name + '%',))
    result = db_cursor.fetchall()
    library = []
    for book in result:
        books_dict = {
            'book_id': book[0],
            'Дата': book[1],
            'Название книги': book[2],
            'Автор': book[3],
            'Новая цена': book[4],
            'Старая цена': book[5],
            'Скидка': book[6],
            'Рейтинг': book[7],
        }
        library.append(books_dict)
    db_cursor.close()
    db_connection.commit()
    return library