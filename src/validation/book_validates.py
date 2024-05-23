def validate_parameters(**kwargs):
    if not any(kwargs.values()):
        raise AttributeError("You need to specify at least one parameter")


def validate_searcher(search_book):
    if not search_book:
        raise ValueError("Book not found")


def validate_inserter(search_book):
    if not search_book:
        raise ValueError("Book already exists")
