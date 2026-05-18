"""AST node defintions for matrix-lang."""
from matrix import *

class Expr:
    """An abstract class representing a matrix-lang expression.
    """
    def evaluate(self):
        """Return the *value* of this expression."""
        raise NotImplementedError

class Scalar(Expr):
    """A numeric literal.

    Instance Attribute:
        - n: the value of the literal
    """
    n: int | float

    def __init__(self, number: int | float) -> None:
        """Initialise a new numeric literal."""
        self.n = number

    def evaluate(self):
        """Return the *value* of this expression.

        >>> expr = Scalar(10.5)
        >>> expr.evaluate()
        10.5
        """
        return self.n

class MatrixLiteral(Expr):
    """A matrix literal.

    Instance Attribute:
        - m: the value of the matrix
    """
    rows: list[list[Expr]]

    def __init__(self, rows: list[list[Expr]]) -> None:
        self.rows = rows

    def evaluate(self):
        rows = [[expr.evaluate() for expr in row] for row in self.rows]
        if all(len(row) == 1 for row in rows):
            return Vector(rows)
        return Matrix(rows)

class BinOp(Expr):
    """An arithmetic binary operation.

    Instance Attributes:
        - left: the left operand
        - op: the name of the operator
        - right: the right operand

    Representation Invariants:
        - self.op in {'+', '*'}
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialise a new binary operation expression.

        Preconditions:
            - op in {'+', '*'}
        """
        self.left = left
        self.op = op
        self.right = right

    # TODO: implement evaluate function
    def evaluate(self):
        """Return the *value* of this expression.

        >>> expr = BinOp(Scalar(10.5), '+', Scalar(30))
        >>> expr.evaluate()
        40.5
        """
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        raise NotImplementedError
