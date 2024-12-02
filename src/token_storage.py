from .token import Token


class TokenStorage:
    def __init__(self):
        """
        Инициализация хранилища токенов.
        """
        self.tokens = {}

    def add_token(self, mint, creation_transaction):
        """
        Добавляет токен в хранилище.
        :param token: Экземпляр класса Token.
        """
        if mint in self.tokens:
            raise ValueError(f"Token with mint {mint} already exists.")
        self.tokens[mint] = Token(creation_transaction)

    def get_token(self, mint):
        """
        Возвращает токен по mint.
        :param mint: Уникальный идентификатор токена (mint).
        :return: Экземпляр класса Token.
        """
        return self.tokens.get(mint, None)

    def remove_token(self, mint):
        """
        Удаляет токен из хранилища по mint.
        :param mint: Уникальный идентификатор токена (mint).
        """
        if mint in self.tokens:
            del self.tokens[mint]
        else:
            raise ValueError(f"Token with mint {mint} not found.")

    def list_tokens(self):
        """
        Возвращает список всех токенов в хранилище.
        :return: Список экземпляров класса Token.
        """
        return list(self.tokens.values())

token_storage = TokenStorage()