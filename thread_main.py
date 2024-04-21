import time
import json
import requests
from bs4 import BeautifulSoup
import threading


def get_elements(num_threads):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    print(f"Старт потока {num_threads}")
    books_list = []

    # Формируем запрос с переходом на новую страницу
    link = f"https://oz.by/books/?page={num_threads}"
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Все карточки товаров
    books_data = soup.find('div', class_="products__grid viewer-type-card--js-active").find_all('article')

    for book in books_data:
        book_header = book.find('div', class_="product-card__body")

        books_dict = {
            'book_title': book_header.find('h3', class_="product-card__title").text.strip(),
            'book_author': book_header.find('div', class_="product-card__subtitle").text.strip(),
            'book_price': str(book_header.find('b', class_="text-primary").text).replace('\xa0', '')
            if book_header.find('b', class_="text-primary") is not None else 'Цена не указана',
            'book_rating': book_header.find('span', class_="me-1").text
            if book_header.find('span', class_="me-1") is not None else 0
        }

        try:
            books_list.append({
                'Название книги': books_dict['book_title'],
                "Автор": books_dict['book_author'],
                "Цена": books_dict['book_price'],
                "Рейтинг": books_dict['book_rating'],
            })
        except AttributeError:
            print("Ошибка в передаче рейтинга")

        print(books_dict)
    print(link)
    print(f"Завершение работы потока {num_threads}")

    with open('thread_library.json', 'w') as file:
        json.dump(books_list, file, indent=4, ensure_ascii=False)


def main():
    threads = []
    for i in range(1, 2):
        thread = threading.Thread(target=get_elements, args=(i,))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    start = time.time()
    main()
    execution_time = time.time() - start
    print(f"Время выполнения: {execution_time} секунд")
