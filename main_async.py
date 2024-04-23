import json
import time
import requests
import asyncio, aiohttp
from bs4 import BeautifulSoup

start = time.time()
books_list = []


async def get_page_data(session, page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    link = f"https://oz.by/books/?page={page}"
    async with session.get(link, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        # Все карточки товаров
        books_data = soup.find('div', class_="products__grid viewer-type-card--js-active").find_all('article')
        for book in books_data:
            book_header = book.find('div', class_="product-card__body")

            # Выведем отдельно каждое поле
            try:
                book_title = book_header.find_all('h3')[0].text.strip()
            except:
                book_title = 'Название отсутствует'

            try:
                book_author = book_header.find('div', class_="product-card__subtitle").text.strip()
            except:
                book_author = 'Автор отсутствует'
            try:
                book_price = book_header.find_all('b')[0].text[0:5] + "р."

            except:
                book_price = 'Цена отсутствует'

            try:
                book_rating = book_header.find('span', class_="me-1").text
            except AttributeError:
                book_rating = 'Рейтинг отсутствует'

            books_list.append(
                {
                    'Название книги': book_title,
                    'Автор': book_author,
                    'Цена': book_price,
                    'Рейтинг': book_rating,
                }
            )
        pages_count = int(soup.find('li', class_="g-pagination__list__li pg-link pg-last").text)
        print(f"Прочтена страница {page} из {pages_count}")



async def get_gather_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    link = "https://oz.by/books/"

    # Сессия клиента для использования открытого соединения
    async with aiohttp.ClientSession() as session:
        response = await session.get(link, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(soup.find('li', class_="g-pagination__list__li pg-link pg-last").text)

        # Список параллельных задач
        tasks = []
        # for page in range(1, pages_count + 1):
        for page in range(1, 11):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(get_gather_data())
    with open('asunc_library.json', 'w') as file:
        json.dump(books_list, file, indent=4, ensure_ascii=False)
    finish = time.time() - start
    print(f"Было затрачено времени: {finish}")


if __name__ == "__main__":
    main()
