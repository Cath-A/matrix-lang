"""Matrix value type for matrix-lang."""
from __future__ import annotations
from errors import *


class Matrix:
    """A matrix value.

    Instance Attributes:
        - rows: the matrix data as a list of lists

    Representation Invariants:
        - len(rows) > 0
        - all(len(row) == len(rows[0]) for row in rows)
    """
    rows: list[list[int | float]]

    def __init__(self, rows: list[list[int | float]]) -> None:
        """Initialise a new matrix."""
        if len(rows) == 0:
            raise ValueError('Matrix cannot be empty')
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError('All rows must be the same length')

        self.rows = rows

    def num_rows(self) -> int:
        """Return the number of rows."""
        return len(self.rows)

    def num_cols(self) -> int:
        """Return the number of columns."""
        return len(self.rows[0])

    def dimensions(self) -> tuple[int, int]:
        """Return the dimensions of the matrix in the form [row, column]."""
        return self.num_rows(), self.num_cols()

    def __neg__(self) -> Matrix:
        """Return the additive inverse of the matrix (-self)."""
        rows = [
            [-value for value in row]
            for row in self.rows
        ]
        return type(self)(rows)

    def __add__(self, other: Matrix) -> Matrix:
        """Return the matrix sum of self and other."""
        if not isinstance(other, Matrix):
            raise MatrixTypeError(f"Cannot add Matrix and {type(other).__name__}")

        if self.dimensions() != other.dimensions():
            raise MatrixShapeError(
                f"Cannot add matrices with shapes "
                f"{self.num_rows()}x{self.num_cols()} and "
                f"{other.num_rows()}x{other.num_cols()}"
            )

        num_rows, num_cols = self.num_rows(), self.num_cols()
        rows = []

        for i in range(num_rows):
            row = [
                self.rows[i][j] + other.rows[i][j]
                for j in range(num_cols)
            ]
            rows.append(row)

        return type(self)(rows)

    def __sub__(self, other: Matrix) -> Matrix:
        """Return the matrix subtraction of self - other."""
        if not isinstance(other, Matrix):
            raise MatrixTypeError(f"Cannot subtract Matrix and {type(other).__name__}")

        return self + (-other)


    def __repr__(self) -> str:
        return f'Matrix({self.rows})'


class Vector(Matrix):
    """A vector value.

    Instance Attributes:
        - rows: the vector data as a list of ints

    Representation Invariants:
        - self.num_cols() == 1
    """
    rows: list[list[int | float]]

    def __init__(self, rows: list[list[int | float]]) -> None:
        """Initialise a new vector."""
        super().__init__(rows)

        if self.num_cols() != 1:
            raise ValueError("Vector must have exactly one column")

    def __repr__(self) -> str:
        return f'Vector({self.rows})'
