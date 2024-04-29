import requests
from celery_config import *
from bs4 import BeautifulSoup


@parser_app.task(name="reading_pages")
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

        book_num = book.get('data-value')
        book_title = book_body.find('h3', class_="product-card__title").text.strip()
        book_author = book_body.find('div', class_="product-card__subtitle").text.strip()
        book_price_first = book_footer.find('b')
        book_price_new = book_body.find('b', class_="text-primary")
        book_price_old = book_body.find('s', class_="d-inline-block text-muted text-decoration-line-through ms-1")
        book_rating = book_body.find('span', class_="me-1")
        book_discount = book_header.find('span', class_="badge badge-sm badge-discount-primary")

        book_data = {
            'book_num': book_num,
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
