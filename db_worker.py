from celery_config import parser_app
from db_config import *


@parser_app.task(name="create_tables")
def create_tables():
    db_cursor = db_connection.cursor()

    db_cursor.execute("SHOW TABLES LIKE 'books'")
    result_books = db_cursor.fetchone()
    if not result_books:
        db_cursor.execute("""
                CREATE TABLE books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE,
                    book_num INT(20) NOT NULL UNIQUE,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    price DECIMAL(10,2),
                    price_old DECIMAL(10,2),
                    discount VARCHAR(20),
                    rating DECIMAL(4,2)
                )
            """)

    db_connection.commit()

    db_cursor.execute("SHOW TABLES LIKE 'books_history'")
    result_books_history = db_cursor.fetchone()
    if not result_books_history:
        db_cursor.execute("""
                   CREATE TABLE books_history (
                        book_id INT(20),
                        FOREIGN KEY (book_id) REFERENCES books(id),
                        date DATE,
                        book_num INT(20),
                        title VARCHAR(255),     
                        price DECIMAL(10,2)

                   )
               """)

    db_cursor.close()
    db_connection.commit()


@parser_app.task(name="write_to_db")
def write_to_db(read_pages):
    db_cursor = db_connection.cursor()

    for line in read_pages:
        for page, books in line.items():
            for book in books:
                book_num = book['book_num']
                title = book['name']
                author = book['author']
                price = book['price']
                price_old = book['price_old']
                discount = book['discount']
                rating = book['rating']
                query_books = """
                        INSERT IGNORE INTO books (date,book_num,title,author,price,price_old,discount,rating)  
                        VALUES (CURDATE(),%s,%s,%s,%s,%s,%s,%s)
                    """
                values_books = [
                    (book_num, title, author, price, price_old, discount, rating),
                ]
                db_cursor.executemany(query_books, values_books)

    db_cursor.close()
    db_connection.commit()


@parser_app.task(name="write_history_to_db")
def write_history_to_db():
    db_cursor = db_connection.cursor()

    db_cursor.execute("""
    INSERT INTO books_history(book_id,`date`,book_num,title,price)
    SELECT id,`date`,book_num,title,price
    FROM books
    WHERE NOT EXISTS (
        SELECT 1 from books_history
        WHERE book_id = books.id and price = books.price)
    """)
    db_cursor.close()
    db_connection.commit()
