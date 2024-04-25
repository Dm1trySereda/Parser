from fastapi import FastAPI
from mysql.connector import connect

app = FastAPI()
db_connection = connect(
    host='db_mysql',
    user='root',
    password='12345',
    database='library'
)


@app.get("/")
async def read_root():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM books")
    result = db_cursor.fetchall()
    library = []
    for book in result:
        books_dict = {
            'Название книги': book[1],
            'Автор': book[2],
            'Цена': book[3],
            'Рейтинг': book[4],
        }
        library.append(books_dict)
        db_cursor.close()
        db_connection.commit()
    return library


# Пагинация
@app.get("/books/")
async def read_root(page: int = 1):
    books_limit = 10
    books_offset = (page - 1) * books_limit  # сколько книг пропускаем
    db_cursor = db_connection.cursor()

    db_cursor.execute("SELECT * FROM books ORDER BY title LIMIT %s OFFSET %s", (books_limit, books_offset))
    result = db_cursor.fetchall()
    library = []
    for book in result:
        books_dict = {
            'Название книги': book[1],
            'Автор': book[2],
            'Цена': book[3],
            'Рейтинг': book[4],
        }
        library.append(books_dict)
        db_cursor.close()
        db_connection.commit()
    return library


# Поиск книги
@app.get("/search")
async def search_books(name: str = None):
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM books WHERE title LIKE %s", ('%' + name + '%',))
    result = db_cursor.fetchall()
    library = []
    for book in result:
        books_dict = {
            'Название книги': book[1],
            'Автор': book[2],
            'Цена': book[3],
            'Рейтинг': book[4],

        }
        library.append(books_dict)
    db_cursor.close()
    db_connection.commit()
    return library
