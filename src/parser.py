"""Converts a token list into an AST.

Raises ParseError on invalid input.
"""
from lexer import Token
from ast import *


def parse(tokens: list[Token]) -> Module:
    """Parse a list of tokens into a Module AST node.

    Returns the root Module representing the full program.
    """
    raise NotImplementedError


def _parse_statement(tokens: list[Token], i: int) -> tuple[Statement, int]:
    """Parse a single statement starting at index i.

    Returns the Statement node and the index of the next unread token.
    """
    raise NotImplementedError


def _parse_assign(tokens: list[Token], i: int) -> tuple[Assign, int]:
    """Parse a single statement starting at index i.

    i should point at the NAME token on the left hand side.
    Returns the Assign node and the index of the next unread token.
    """
    raise NotImplementedError


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
    ."""
    raise NotImplementedError


def _parse_atom(tokens: list[Token], i: int) -> tuple[Expr, int]:
    """Parse an atomic expression starting at index i.

     Handles scalars, names, function calls, matrix literals, and
     parenthesised expressions. Never call directly - called by _parse_multiplication.
     Returns the Expr node and the index of the next unread token.
    """
    raise NotImplementedError
