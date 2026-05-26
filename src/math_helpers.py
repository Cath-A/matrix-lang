"""Mathematical helper functions for matrix-lang.

Contains standalone algorithm implementations used by the Matrix class.
These are separated to keep matrix.py readable and to make the algorithms independently testable.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matrix import Matrix


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Return the matrix product of ab.

    Preconditions:
        - a.num_cols() == b.num_rows()
    """
    return type(a)([
        [
            sum(a[i, k] * b[k, j] for k in range(a.num_cols()))
            for j in range(b.num_cols())
        ]
        for i in range(a.num_rows())
    ])
