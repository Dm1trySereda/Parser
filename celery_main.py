import os
import requests
from celery import Celery, group, chain
from bs4 import BeautifulSoup
from mysql.connector import connect

# Main name дается такой же как и название файла, иначе необходимо указывать рядом с каждой таской ее имя в виде (name="task_name")
broker_url = os.getenv('BROKER_URL')
backend_url = os.getenv('RESULT_BACKEND')
parser = Celery(
    'celery_main',
    broker=broker_url,
    backend=backend_url,
    include=['celery_main'],

)

user_name = os.getenv('MYSQL_USER')
user_password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DATABASE')

db_connection = connect(
    host="db_mysql",
    user='root',
    password='12345',
    database='library',
)


@parser.task()
def reading_pages(page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    library = list()
    print(f"Читаем страницу {page}")

    # Формируем запрос с переходом на новую страницу
    link = f"https://oz.by/books/?page={page}"
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Все карточки товаров
    all_books = soup.find('div', class_="products__grid viewer-type-card--js-active").find_all('article')

    for book in all_books:
        book_header = book.find('div', class_="product-card__body")

        book_title = book_header.find('h3', class_="product-card__title").text.strip()
        book_author = book_header.find('div', class_="product-card__subtitle").text.strip()
        book_price = book_header.find('b', class_="text-primary")
        book_rating = book_header.find('span', class_="me-1")

        book_data = {
            'Название книги': book_title,
            'Автор': book_author,
            'Цена': book_price.text.replace('\xa0', '').rstrip('р.').replace(',', '.') if book_price else None,
            'Рейтинг': book_rating.text.replace(',', '.') if book_rating else None,
        }
        library.append(book_data)
    all_books_in_page = {f"Страница {page}": library}
    return all_books_in_page


@parser.task()
def create_table():
    db_cursor = db_connection.cursor()

    db_cursor.execute("SHOW TABLES LIKE 'books'")
    result = db_cursor.fetchone()

    # Если таблица books не существует, создаем ее
    if not result:
        db_cursor.execute("""
                CREATE TABLE books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    page VARCHAR(255),
                    title VARCHAR(255),
                    author VARCHAR(255),
                    price DECIMAL(10,2),
                    rating DECIMAL(4,2)
                )
            """)

    db_cursor.close()


@parser.task()
def write_to_db(result_pages):
    db_cursor = db_connection.cursor()

    for item in result_pages:
        for key, value in item.items():
            for book in value:
                title = book['Название книги']
                author = book['Автор']
                price = book['Цена']
                rating = book['Рейтинг']
                query = """
                        INSERT INTO books (page, title, author, price, rating)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                values = [
                    (key, title, author, price, rating),
                ]
                db_cursor.executemany(query, values)

    db_cursor.close()
    db_connection.commit()


def main():
    tasks_group = group(reading_pages.s(i) for i in range(1, 11))
    tasks_chain = chain(tasks_group, write_to_db.s())
    create_table.delay()
    result = tasks_chain.delay()
    result.get()


if __name__ == '__main__':
    main()
