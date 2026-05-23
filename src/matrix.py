"""Matrix value type for matrix-lang."""

# TODO: add __str__ function
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
