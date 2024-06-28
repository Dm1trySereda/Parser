class DomainError(Exception):
    """Базовое исключение для доменных ошибок."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ProvidingParametersError(DomainError):
    """Исключение, выбрасываемое, если не предоставлены параметры поиска."""

    def __init__(self):
        super().__init__("You need to specify at least one parameter")


class ResultError(DomainError):
    """Исключение, выбрасываемое, если поиск не дал результат."""

    def __init__(self):
        super().__init__("Books not found")


class DuplicateError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("Book already exist")


class BookHistoryError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("This book has no price history")


class UnauthorizedError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("Incorrect username or password")


class RemoteTokenError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("Received an unexpected status from Google")


class UsernameError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("User with this username already exists")


class EmailError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("This email address is already in use maybe you need to auth")


class OTPCodeError(DomainError):
    """Исключение, выбрасываемое, если книга уже существует."""

    def __init__(self):
        super().__init__("Invalid confirmation code")
