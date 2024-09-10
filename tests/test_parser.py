from project2.parser import _Parser
from project2.token import Token


def test_given_token_iterator_when_match_token_then_stutter_last_token():
    # given
    token_list = [Token.colon(":"), Token.eof("")]
    token_iterator = iter(token_list)
    parser = _Parser(token_iterator)

    # when
    parser._match_token("COLON")
    # then
    assert parser._token == Token.eof("")

    # when
    parser._match_token("EOF")
    # then
    assert parser._token == Token.eof("")

    # when
    parser._match_token("EOF")
    # then
    assert parser._token == Token.eof("")
