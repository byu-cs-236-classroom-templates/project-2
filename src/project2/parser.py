from typing import Iterator

from project2.token import Token


class DatalogProgram:
    pass


class UnexpectedTokenException(Exception):
    __slots__ = ["expected_token", "token"]

    def __init__(
        self,
        expected_token: Token,
        token: Token,
        message: str = "A parse error occurred due to an unexpected token",
    ) -> None:
        super().__init__(message)
        self.expected_token = expected_token
        self.token = token


def parser(token_iterator: Iterator[Token]) -> DatalogProgram:
    raise NotImplementedError
