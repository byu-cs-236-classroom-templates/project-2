"""Parser for Datalog programs.

Provides the parser and error interface for when parsing fails for Datalog
programs.
"""

from typing import Iterator

from project2.token import Token, TokenType
from project2.datalogprogram import DatalogProgram


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


class _Parser:
    """Container for the Datalog program parser.

    The parser is a collection of functions with each function representing a grammar
    rule the Datalog grammar. Each function returns the datatype associated with the
    grammar rule. For example, the rules for a `scheme` is implemented by the `_scheme`
    function that should return a `Predicate` for the scheme if it parses correctly.
    The input is courtesy of an iterator over tokens. The iterator comes from the lexer.
    As an important note, the last token in the token stream is repeated over and over
    again so technically, the token stream has no end.

    Attributes:
        _token_iterator: The `Iterator[Token]` that comes from the lexer.
        _token: the current token to _check_ or _match_.
    """

    __slots__ = ["_token_iterator", "_token"]

    def __init__(self, token_iterator: Iterator[Token]) -> None:
        self._token_iterator = token_iterator
        self._update_token()

    def _check_token(self, token_type: TokenType) -> bool:
        """Returns true iff the specified type matches the current token.

        `_check_token` is a way to _peek_ at a token without consuming that it.
        It is especially useful for follow sets when it is necessary to see if
        something in the follow set is coming. For example, for the Kleene star
        for zero or more repetitions as would be used in a list, what follows
        indicates if another repetition happens or not. `_check_token` is
        intended just for that determination.

        Args:
            token_type: The expected token type in the stream for a successful parse.

        Returns:
            out: True iff the current token type matches the expected token type.
        """
        return token_type == self._token.token_type

    def _match_token(self, token_type: TokenType) -> None:
        """Matches and updates the token.

        `_match_token` consumes the current token iff it matches the expected
        type. The parser uses this to _consume_ tokens from the token stream
        until it completes a Datalog program. If ever the consumed token does
        not match the expected token type, it raises an exception indicating
        a parse failure.

        Args:
            token_type: The expected token type in the stream for a successful parse.

        Raises:
            error (UnexpectedTokenException): Parse error if the token type does not match the expected token type.
        """
        if self._token.token_type != token_type:
            raise UnexpectedTokenException(token_type, self._token)
        self._update_token()

    def _update_token(self) -> None:
        """Advances the iterator and updates the token.

        The last token in the iterator is stuttered meaning that it is repeated
        on every subsequent call.
        """
        try:
            self._token = next(self._token_iterator)
        except StopIteration:
            pass

    def _datalog_program(self) -> DatalogProgram:
        """Top-level grammar rule for a Datalog program.

        The function directly matches its associated grammar rule by matching
        on keywords and collecting returns from other non-terminal rules to
        build an instance of a `DatalogProgram`.

        Pseudo-code:
        ```
        self._match_token('SCHEMES')
        self._match_token('COLON')
        schemes: list[Predicate] = [self._scheme()]
        schemes.extend(self._scheme_list())

        # Other matches and function calls for the rest of a Datalog Program

        return DatalogProgram(schemes, facts, rules, queries)
        ```

        Returns:
            program: The Datalog program from the parse.
        """
        raise NotImplementedError

    def parse(self) -> DatalogProgram:
        """Helper function to call the starting rule."""
        return self._datalog_program()


def parse(token_iterator: Iterator[Token]) -> DatalogProgram:
    """Parse a datalog program.

    A convenience function that avoids having to create an instance of the
    `_Parser` class.
    """
    return _Parser(token_iterator).parse()
