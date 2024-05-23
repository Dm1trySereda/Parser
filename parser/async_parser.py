import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def reading_session(page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        return await parsing_books(page, session)


async def parsing_books(page, session):
    library = list()
    link = f"https://oz.by/books/?page={page}"
    try:
        async with session.get(link) as response:
            response_test = await response.text()
            soup = BeautifulSoup(response_test, "lxml")
            all_books = soup.find(
                "div", class_="products__grid viewer-type-card--js-active"
            ).find_all("article")
    except AttributeError:
        print(f"Return NoneType object,page-->{page}")
        return None
    for book in all_books:
        book_header = book.find("div", class_="product-card__header")
        book_body = book.find("div", class_="product-card__body")
        book_footer = book.find("div", class_="product-card__cost")

        book_price_new = validation(book_footer.find("b"), is_price=True)
        if book_price_new is None:
            continue

        book_price_old = validation(
            book_body.find(
                "s",
                class_="d-inline-block text-muted text-decoration-line-through ms-1",
            ),
            is_price=True,
        )
        book_num = book.get("data-value")
        book_title = book_body.find("h3", class_="product-card__title").text.strip()
        book_author = book_body.find(
            "div", class_="product-card__subtitle"
        ).text.strip()
        book_rating = validation(book_body.find("span", class_="me-1"), is_rating=True)
        book_discount = None
        if book_price_old:
            book_discount = (
                str(round(100 - (float(book_price_new) * 100 / float(book_price_old))))
                + "%"
            )
        book_image = validation(
            book_header.find("img", class_="product-card__cover-image"), is_image=True
        )

        book_data = {
            "book_num": book_num,
            "title": book_title,
            "author": book_author,
            "price_new": book_price_new,
            "price_old": book_price_old,
            "discount": book_discount,
            "rating": book_rating,
            "image_url": book_image,
        }
        library.append(book_data)

    return library


def validation(value, is_price=False, is_rating=False, is_image=False):
    if value:
        if is_price:
            value = (
                value.text.replace("\xa0", "").rstrip("р.").replace(",", ".").strip()
            )
        elif is_rating:
            value = value.text.replace(",", ".")
        elif is_image:
            value = value.get("src")
        return value
    return None


#
# async def start_reading(page):
#     # result = await parsing_books(page, session)
#     # return result
#     pages = [reading_session(i) for i in range(1, page + 1)]
#     all_pages = list()
#     for page in asyncio.as_completed(pages):
#         result = all_pages.append(await page)
#     return all_pages


# if __name__ == "__main__":
#     print(asyncio.run(reading_session(10)))
