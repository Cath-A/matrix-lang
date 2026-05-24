"""Custom exception for matrix-lang runtime and matrix operation errors."""


class MatrixError(Exception):
    """Base class for matrix-lang runtime errors."""


class MatrixShapeError(MatrixError):
    """Raised when matrix dimensions"""


class MatrixTypeError(MatrixError):
    """Raised when matrix operations are applied to invalid types."""
