"""Converts a token list into an AST.

Raises ParseError on invalid input.
"""
from lexer import Token, TokenType
from ast import *


def parse(tokens: list[Token]) -> Module:
    """Parse a list of tokens into a Module AST node.

    Returns the root Module representing the full program.
    """
    body = []
    i = 0

    while tokens[i].type != TokenType.EOF:
        while tokens[i].type == TokenType.NEWLINE:
            i += 1
            if tokens[i].type == TokenType.EOF:
                break

        statement, i = _parse_statement(tokens, i)
        body.append(statement)

        if tokens[i].type == TokenType.NEWLINE:
            i += 1
        elif tokens[i].type != TokenType.EOF:
            raise SyntaxError(f"Unexpected token: {tokens[i].value}")

    return Module(body)


def _parse_statement(tokens: list[Token], i: int) -> tuple[Statement, int]:
    """Parse a single statement starting at index i.

    Returns the Statement node and the index of the next unread token.
    """
    # assignment: NAME = expr
    if (
        tokens[i].type == TokenType.NAME
        and tokens[i + 1].type == TokenType.EQUALS
    ):
        return _parse_assign(tokens, i)

    # otherwise parse as expression
    return _parse_addition(tokens, i)


def _parse_assign(tokens: list[Token], i: int) -> tuple[Assign, int]:
    """Parse an assignment statement starting at index i.

    `i` should point at the NAME token on the left hand side.
    Representation Invariants:
        - tokens[i].type == TokenType.NAME
        - tokens[i + 1].type == TokenType.EQUALS
        - tokens[i + 2:] begins a valid expression
        - this function is only called by _parse_statement for assignment cases

    Returns the Assign node and the index of the next unread token.
    """
    target = tokens[i].value
    i += 2
    value, i = _parse_addition(tokens, i)

    # forbid chained assignment: must end statement here
    if tokens[i].type not in (TokenType.NEWLINE, TokenType.EOF):
        raise SyntaxError("Chained assignment is not allowed")

    return Assign(target, value), i


def _parse_addition(tokens: list[Token], i: int) -> tuple[Expr, int]:
    """Parse an addition or subtraction expression starting at index i.

    Entry point for all expression parsing - always call this first.
    Returns the Expr node at the index of the next unread token.
    """
    raise NotImplementedError


def _parse_multiplication(tokens: list[Token], i: int) -> tuple[Expr, int]:
    """Parse a multiplication or division expression starting at index i

    Never call directly - called by _parse_addition.
    Returns the Expr node and the index of the next unread token.
    """
    raise NotImplementedError


def _parse_atom(tokens: list[Token], i: int) -> tuple[Expr, int]:
    """Parse an atomic expression starting at index i.

     Handles scalars, names, function calls, matrix literals, and
     parenthesised expressions. Never call directly - called by _parse_multiplication.
     Returns the Expr node and the index of the next unread token.
    """
    raise NotImplementedError
