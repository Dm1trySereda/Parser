from celery import Celery
from celery import group, chain

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task(name='add')
def add(x, y):
    return x + y


@app.task(name='multiply')
def multiply(x, y):
    return x * y


@app.task(name='minus')
def minus(x, y):
    return x - y


def main():
    # chain = add.s(2, 2) | multiply.s(3) | minus.s(10)
    # result = chain.apply_async()
    g = group(add.s(i, i) for i in range(10))().get()


if __name__ == '__main__':
    main()
