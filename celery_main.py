import requests, json, time

from bs4 import BeautifulSoup
from celery import Celery, group, chain

# Main name дается такой же как и название файла, иначе необходимо указывать рядом с каждой таской ее имя в виде (name="task_name")
parser = Celery(
    'celery_main',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['celery_main'],

)


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
            'Цена': book_price.text.replace('\xa0', '') if book_price else 'Цена не указана',
            'Рейтинг': book_rating.text if book_rating else 'Рейтинг не указан',
        }
        library.append(book_data)
    all_books_in_page = {f"Страница {page}": library}
    return all_books_in_page


@parser.task()
def first_part_pages(start, end):
    result = []
    for i in range(start, end):
        result.append(reading_pages(i))
    return result


@parser.task()
def second_part_pages(start, end):
    result = []
    for i in range(start, end):
        result.append(reading_pages(i))
    return result


@parser.task()
def write_to_json(result_pages):
    with open('read_page.json', 'a') as file:
        json.dump(result_pages, file, indent=4, ensure_ascii=False)
        file.write('\n')


def main():
    result1 = first_part_pages.delay(1, 6).get()
    result2 = second_part_pages.delay(6, 11).get()
    combined_result = result1 + result2
    write_to_json.apply_async(args=[combined_result])


if __name__ == '__main__':
    main()
