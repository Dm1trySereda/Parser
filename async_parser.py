import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def parse_the_page(page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    library = list()
    link = f"https://oz.by/books/?page={page}"
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as response:
            response_test = await response.text()
            soup = BeautifulSoup(response_test, 'lxml')
            all_books = soup.find('div', class_="products__grid viewer-type-card--js-active").find_all('article')
            for book in all_books:
                book_header = book.find('div', class_="product-card__header")
                book_body = book.find('div', class_="product-card__body")
                book_footer = book.find('div', class_="product-card__cost")

                book_num = book.get('data-value')
                book_title = book_body.find('h3', class_="product-card__title").text.strip()
                book_author = book_body.find('div', class_="product-card__subtitle").text.strip()
                book_price = validation(book_footer.find('b'), is_price=True)
                book_price_old = validation(
                    book_body.find('s', class_="d-inline-block text-muted text-decoration-line-through ms-1"),
                    is_price=True)
                book_rating = validation(book_body.find('span', class_="me-1"), is_rating=True)
                book_discount = validation(
                    book_header.find('span', class_="badge badge-sm badge-discount-primary"),
                    is_discount=True)
                book_image = validation(book_header.find('img', class_="product-card__cover-image"), is_image=True)

                book_data = {
                    'book_num': book_num,
                    'name': book_title,
                    'author': book_author,
                    'price': book_price,
                    'price_old': book_price_old,
                    'discount': book_discount,
                    'rating': book_rating,
                    'image': book_image
                }
                library.append(book_data)
            all_books_in_page = {f"Страница {page}": library}
            return all_books_in_page


def validation(value, is_price=False, is_rating=False, is_discount=False, is_image=False):
    if value:
        if is_price:
            value = value.text.replace('\xa0', '').rstrip('р.').replace(',', '.').strip()
        elif is_rating:
            value = value.text.replace(',', '.')
        elif is_discount:
            value = value.text.strip()
        elif is_image:
            value = value.get('src')
        return value
    return None


# async def start_reading(page):
#     async with aiohttp.ClientSession() as session:
#         result = await parse_the_page(page, session)
#         return result
#         # pages = [parse_the_page(i, session) for i in range(1, page + 1)]
#         # all_pages = list()
#         # for page in asyncio.as_completed(pages):
#         #     result = all_pages.append(await page)
#         # return all_pages


if __name__ == "__main__":
    print(asyncio.run(parse_the_page(10)))
