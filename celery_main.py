import os
import requests
from celery import Celery, group, chain
from bs4 import BeautifulSoup
from mysql.connector import connect
from dotenv import load_dotenv

load_dotenv()

# Main name дается такой же как и название файла, иначе необходимо указывать рядом с каждой таской ее имя в виде (name="task_name")

parser = Celery(
    'celery_main',
    broker=os.getenv('BROKER_URL'),
    backend=os.getenv('RESULT_BACKEND'),
    include=['celery_main'],

)

db_connection = connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)


@parser.task()
def reading_pages(page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    library = list()
    # Формируем запрос с переходом на новую страницу
    link = f"https://oz.by/books/?page={page}"
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    all_books = soup.find('div', class_="products__grid viewer-type-card--js-active").find_all('article')
    for book in all_books:
        book_header = book.find('div', class_="product-card__header")
        book_body = book.find('div', class_="product-card__body")
        book_footer = book.find('div', class_="product-card__cost")

        book_id = book.get('data-value')
        book_title = book_body.find('h3', class_="product-card__title").text.strip()
        book_author = book_body.find('div', class_="product-card__subtitle").text.strip()
        book_price_first = book_footer.find('b')
        book_price_new = book_body.find('b', class_="text-primary")
        book_price_old = book_body.find('s', class_="d-inline-block text-muted text-decoration-line-through ms-1")
        book_rating = book_body.find('span', class_="me-1")
        book_discount = book_header.find('span', class_="badge badge-sm badge-discount-primary")

        book_data = {
            'book_id': book_id,
            'name': book_title,
            'author': book_author,
            'price': book_price_first.text.replace('\xa0', '').rstrip('р.').replace(',',
                                                                                    '.').strip() if book_price_first else None,
            'price_old': book_price_old.text.replace('\xa0', '').rstrip('р.').replace(',',
                                                                                      '.').strip() if book_price_old else None,
            'discount': book_discount.text.strip() if book_discount else None,
            'rating': book_rating.text.replace(',', '.') if book_rating else None,
        }
        library.append(book_data)
    all_books_in_page = {f"Страница {page}": library}
    return all_books_in_page


@parser.task()
def create_tables():
    db_cursor = db_connection.cursor()

    db_cursor.execute("SHOW TABLES LIKE 'books'")
    result_books = db_cursor.fetchone()
    if not result_books:
        db_cursor.execute("""
                CREATE TABLE books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE,
                    book_id INT(20),
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
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        book_id INT(20),
                        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                        date DATE,
                        price DECIMAL(10,2)
                      
                   )
               """)

    db_connection.commit()

    db_cursor.close()
    # В истории хранить данные цен на книги, если цена книги изменилась - добавить запись в историю


@parser.task()
def write_to_db(result_pages):
    db_cursor = db_connection.cursor()

    for item in result_pages:
        for key, value in item.items():
            for book in value:
                book_id = book['book_id']
                title = book['name']
                author = book['author']
                price = book['price']
                price_old = book['price_old']
                discount = book['discount']
                rating = book['rating']
                query = """
                        INSERT INTO books (date,book_id,title,author,price,price_old,discount,rating)
                        VALUES (CURDATE(),%s,%s,%s,%s,%s,%s,%s)
                    """
                values = [
                    (book_id, title, author, price, price_old, discount, rating),
                ]
                db_cursor.executemany(query, values)

    db_cursor.close()
    db_connection.commit()


def main():
    tasks_group = group(reading_pages.s(i) for i in range(1, 101))
    tasks_chain = chain(tasks_group, write_to_db.s())
    create_tables.delay()
    result = tasks_chain.delay()
    result.get()


if __name__ == '__main__':
    main()
