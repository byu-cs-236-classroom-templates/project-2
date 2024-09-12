"""Parser for Datalog programs.

Provides the parser and error interface for when parsing fails for Datalog
programs.
"""

from typing import Iterator

from project2.token import Token, TokenType
from project2.datalogprogram import DatalogProgram, Parameter


class UnexpectedTokenException(Exception):
    """Class for parsing errors.

    A parse error is when the actual token does not have the correct type
    according to the state of the parser. In other words, the parser is
    expecting a specific token type but the actual token at that point does
    not match the expected type.

    Attributes:
        expected_types: The type that was expected in the parse.
        token: The actual token that was encountered.
    """

    __slots__ = ["expected_type", "token"]

    def __init__(
        self,
        expected_type: TokenType,
        token: Token,
        message: str = "A parse error occurred due to an unexpected token",
    ) -> None:
        super().__init__(message)
        self.expected_type = expected_type
        self.token = token


class TokenStream:
    __slots__ = ["token", "_token_iterator"]

    def __init__(self, token_iterator: Iterator[Token]) -> None:
        self._token_iterator = token_iterator
        self.advance()

    def __repr__(self) -> str:
        return f"TokenStream(token={self.token!r}, _token_iterator={self._token_iterator!r})"

    def advance(self) -> None:
        """Advances the iterator and updates the token.

        The last token in the iterator is stuttered meaning that it is repeated
        on every subsequent call.
        """
        try:
            self.token = next(self._token_iterator)
        except StopIteration:
            pass

    def match(self, token_type: TokenType) -> None:
        """Return if token matches expected type.

        `match` returns iff the expected type matches the current taken. If
        ever the token does not match the expected type, it raises an exception
        indicating a match failure.

        Args:
            token_type: The expected token type in the stream for a successful parse.

        Raises:
            error (UnexpectedTokenException): Match error if the token type does not match the expected token type.
        """
        if self.token.token_type != token_type:
            raise UnexpectedTokenException(token_type, self.token)

    def member_of(self, token_types: set[TokenType]) -> bool:
        """Returns true iff the current token type is in the specified type.

        `member_of` is a way to determine if the type of the current token is
        in a set of token types. It is especially useful for checking membership
        in first and follow sets when implementing a table driven parser.

        Args:
            token_types: A set of token types.

        Returns:
            out: True iff the current token type is in the set of token types.
        """
        return self.token.token_type in token_types

    def value(self) -> str:
        """Return the value attribute of the current token."""
        return self.token.value


def comma(token: TokenStream) -> None:
    token.match("COMMA")
    token.advance()


def datalog_program(token: TokenStream) -> DatalogProgram:
    """Top-level grammar rule for a Datalog program.

    The function directly matches its associated grammar rule by matching
    on keywords and collecting returns from other non-terminal rules to
    build an instance of a `DatalogProgram`.

    Pseudo-code:
    ```
    token.match('SCHEMES')
    token.advance()
    token.match_token('COLON')
    token.advance()

    schemes: list[Predicate] = [scheme(token)]
    schemes.extend(scheme_list(token))

    # Other matches, advances, and rules for the rest of a Datalog Program

    return DatalogProgram(schemes, facts, rules, queries)
    ```

    Returns:
        program: The Datalog program from the parse.
    """

    raise NotImplementedError


def id(token: TokenStream) -> Parameter:
    token.match("ID")
    parameter = Parameter.id(token.value())
    token.advance()
    return parameter


def id_list(token: TokenStream, ids: list[Parameter] = []) -> list[Parameter]:
    """Parse and build a list of ID parameters from a stream.

    ```
    id_list
        : COMMA id
        | lambda
        ;
    ```

    Here is the context fro the `id_list` rule: `LEFT_PAREN id id_list RIGHT_PAREN`
    The follow set is checked to account for the lambda reduction on the list.
    After that, the `TokenStream.match` raises an exception if the token does not match.
    It is equivalent to the following code:

    ```
    if token.token.token_type != "ID":
        raise UnexpectedTokenException("ID", token.token)
    ```

    The `TokenStream.match` avoids having to write the same check for every rule.

    Args:
        token: The token stream.
        ids: The current set of parameters from the parse.

    Returns:
        out: the list of ID parameters from the parse.
    """
    follow: set[TokenType] = {"RIGHT_PAREN"}

    if token.member_of(follow):
        return ids

    comma(token)
    parameter = id(token)
    ids.append(parameter)

    return id_list(token, ids)


def parse(token_iterator: Iterator[Token]) -> DatalogProgram:
    """Parse a datalog program.

    A convenience function that avoids having to create an instance of the
    `_Parser` class.
    """
    token: TokenStream = TokenStream(token_iterator)
    return datalog_program(token)
