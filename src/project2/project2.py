from sys import argv
from typing import Iterator

from project2.token import Token
from project2.lexer import lexer
from project2.parser import parser, DatalogProgram, UnexpectedTokenException


def project2(input_string: str) -> str:
    token_iterator: Iterator[Token] = lexer(input_string)

    try:
        datalog_program: DatalogProgram = parser(token_iterator)
        return "Success!\n" + str(datalog_program)
    except UnexpectedTokenException as e:
        return "Failure!\n  " + str(e.token)


def project2cli() -> None:
    """Build the DatalogProgram from the contents of a file."""
    if len(argv) == 2:
        input_file = argv[1]
        with open(input_file, "r") as f:
            input_string = f.read()
            result = project2(input_string)
            print(result)
    else:
        print("usage: project2 <input file>")
