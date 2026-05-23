"""AST node defintions for matrix-lang."""

from typing import Any, Optional
from matrix import *


class Statement:
    """An abstract class representing a matrix-lang statement.

    We think of a statement as being a more general piece of code than a
    single expression, and that can have some kind of "effect".
    """
    def evaluate(self, env: dict[str, Any]) -> Optional[Any]:
        """Evaluate this statement with the given environment.

        Note that the return type here is Optional[Any]: evaluating a statement
        could produce a value (this is true for all expressions), but it might
        only have a *side effect* like mutating `env` or printing something.
        """
        raise NotImplementedError

# Statements
class Expr(Statement):
    """An abstract class representing a matrix-lang expression.
    """
    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression."""
        raise NotImplementedError


class Assign(Statement):
    """An assignment statement (with a single target).

    Instance Attributes:
        - target: the variable name on the left-hand side of the equals sign
        - value: the expression on the right-hand side of the equals sign
    """
    target: str
    value: Expr

    def __init__(self, target: str, value: Expr) -> None:
        """Initialise a new Assign node."""
        self.target = target
        self.value = value

    def evaluate(self, env: dict[str, Any]) -> None:
        """Evaluate this statement with the given environment.
        """
        env[self.target] = self.value.evaluate(env)


class Print(Statement):
    """A statement representing a call to the `print` function.

    Instance Attributes:
        - argument: The argument expression to the `print` function.
    """
    def __init__(self, argument: Expr) -> None:
        """Initialise a new Print node."""
        self.argument = argument

    def evaluate(self, env: dict[str, Any]) -> None:
        """Evaluate this statement.

        This evaluates the argument of the print call, and then actually
        prints it. Note that it doesn't return anything, since `print` doesn't
        return anything.
        """
        print(self.argument.evaluate(env))


# Control flow statements
class If(Statement):
    """An if statement.

    This is a statement of the form:
        if <test>:
            <body>
        else:
            <orelse>

    Instance Attributes:
        - test: The condition expression of this if statement.
        - body: A sequence of statements to evaluate if the condition is True.
        - orelse: A sequence of statements to evaluate if the condition is False.
                    (This would be empty in the case that there is no `else` block.)
    """
    test: Expr
    body: list[Statement]
    orelse: list[Statement]

    def __init__(self, test: Expr, body: list[Statement], orelse: list[Statement]) -> None:
        """Initialise a new If node."""
        self.test = test
        self.body = body
        self.orelse = orelse

    def evaluate(self, env: dict[str, Any]) -> None:
        """Evaluate this if statement with the given environment.

        Evaluates the test condition and executes the body if True, otherwise
        executes the orelse block.
        """
        test_result = self.test.evaluate(env)
        if test_result:
            for statement in self.body:
                statement.evaluate(env)
        else:
            for statement in self.orelse:
                statement.evaluate(env)


class ForRange(Statement):
    """A for loop that loops over a range of numbers.

    for <target> in range(<start>, <stop>):
        <body>

    Instance Attributes:
        - target: The loop variable.
        - start: The start for the range (inclusive).
        - stop: The end of the range (this is *exclusive*, so <stop> is not included
                in the loop).
        - body: The statements to execute in the loop body.
    """
    target: str
    start: Expr
    stop: Expr
    body: list[Statement]

    def __init__(self, target: str, start: Expr, stop: Expr, body: list[Statement]) -> None:
        """Initialise a new ForRange node."""
        self.target = target
        self.start = start
        self.stop = stop
        self.body = body

    def evaluate(self, env: dict[str, Any]) -> None:
        """Evaluate this statement with the given environment."""
        start_val = self.start.evaluate(env)
        stop_val = self.stop.evaluate(env)
        for i in range(start_val, stop_val):
            env[self.target] = i
            for statement in self.body:
                statement.evaluate(env)

# Expressions
class Scalar(Expr):
    """A numeric literal.

    Instance Attribute:
        - n: the value of the literal
    """
    n: int | float

    def __init__(self, number: int | float) -> None:
        """Initialise a new numeric literal."""
        self.n = number

    def evaluate(self, env: dict[str, Any]) -> Any:
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

    def evaluate(self, env: dict[str, Any]) -> Any:
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
            - op in {'+', '-', '*', '/'}
        """
        self.left = left
        self.op = op
        self.right = right

    # TODO: implement evaluate function
    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        >>> expr = BinOp(Scalar(10.5), '+', Scalar(30))
        >>> expr.evaluate()
        40.5
        """
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        raise NotImplementedError


class Name(Expr):
    """A variable expression.

    Instance Attributes:
        - id: The variable name.
    """
    id: str

    def __init__(self, id_: str) -> None:
        """Initialise a new variable expression."""
        self.id = id_

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Return the *value* of this expression.

        The name should be looked up in the `env` argument to this method.
        Raise a NameError if the name is not found.
        """
        if self.id in env:
            return env[self.id]
        else:
            raise NameError(f"name '{self.id}' is not defined")


class FuncCall(Expr):
    """A function call expression.

    Instance Attributes:
        - name: the name of the function
        - args: the list of arguments
    """
    name: str
    args: list[Expr]

    def __init__(self, name: str, args: list[Expr]) -> None:
        """Initialise a new FuncCall node."""
        self.name = name
        self.args = args

    # TODO: implement FuncCall evaluate
    def evaluate(self, env: dict[str, Any]) -> Any:
        """Evaluate this function call."""
        raise NotImplementedError


# Module
class Module:
    """A class representing a full matrix-lang program.

    Instance Attributes:
        - body: A sequence of statements.
    """
    body: list[Statement]

    def __init__(self, body: list[Statement]) -> None:
        """Initialise a new module with the given body."""
        self.body = body

    def evaluate(self) -> None:
        """Evaluate this statement with the given environment.
        """
        env = {}
        for statement in self.body:
            statement.evaluate(env)
