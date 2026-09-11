"""Abstract Syntax Tree node definitions for the ultra high-level language."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ASTNode(ABC):
    """Base class for all AST nodes."""

    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for code generation or other operations."""
        pass


class Expression(ASTNode):
    """Base class for expressions."""

    pass


class Literal(Expression):
    """Represents a literal value (number, string, boolean)."""

    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __repr__(self):
        return f"Literal({self.value})"


class Identifier(Expression):
    """Represents a variable identifier."""

    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_identifier(self)

    def __repr__(self):
        return f"Identifier({self.name})"


class BinaryOp(Expression):
    """Represents a binary operation."""

    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_op(self)

    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"


class UnaryOp(Expression):
    """Represents a unary operation."""

    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_op(self)

    def __repr__(self):
        return f"UnaryOp({self.operator} {self.operand})"


class ListLiteral(Expression):
    """Represents a list literal."""

    def __init__(self, elements: List[Expression]):
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_list_literal(self)

    def __repr__(self):
        return f"ListLiteral({self.elements})"


class Statement(ASTNode):
    """Base class for statements."""

    pass


class VariableDeclaration(Statement):
    """Represents a variable declaration with optional type."""

    def __init__(self, name: str, value: Expression, var_type: Optional[str] = None):
        self.name = name
        self.value = value
        self.var_type = var_type

    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

    def __repr__(self):
        type_str = f": {self.var_type}" if self.var_type else ""
        return f"VariableDeclaration({self.name}{type_str} = {self.value})"


class Assignment(Statement):
    """Represents a variable assignment."""

    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def __repr__(self):
        return f"Assignment({self.name} = {self.value})"


class Loop(Statement):
    """Base class for loops."""

    pass


class ForLoop(Loop):
    """Represents a 'for each' loop."""

    def __init__(self, item_var: str, iterable: Expression, body: List[Statement]):
        self.item_var = item_var
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_loop(self)

    def __repr__(self):
        return f"ForLoop({self.item_var} in {self.iterable})"


class WhileLoop(Loop):
    """Represents a 'while' loop."""

    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_loop(self)

    def __repr__(self):
        return f"WhileLoop({self.condition})"


class RepeatLoop(Loop):
    """Represents a 'repeat N times' loop."""

    def __init__(self, count: Expression, body: List[Statement]):
        self.count = count
        self.body = body

    def accept(self, visitor):
        return visitor.visit_repeat_loop(self)

    def __repr__(self):
        return f"RepeatLoop({self.count} times)"


class IfStatement(Statement):
    """Represents an if/else statement."""

    def __init__(
        self,
        condition: Expression,
        then_body: List[Statement],
        else_body: Optional[List[Statement]] = None,
    ):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []

    def accept(self, visitor):
        return visitor.visit_if_statement(self)

    def __repr__(self):
        return f"IfStatement({self.condition})"


class PrintStatement(Statement):
    """Represents a print/display statement."""

    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_statement(self)

    def __repr__(self):
        return f"PrintStatement({self.expression})"


class InputStatement(Statement):
    """Represents a user input statement."""

    def __init__(self, name: str, prompt: Optional[Expression] = None):
        self.name = name
        self.prompt = prompt

    def accept(self, visitor):
        return visitor.visit_input_statement(self)

    def __repr__(self):
        return f"InputStatement({self.name})"


class Program(ASTNode):
    """Represents the entire program."""

    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)

    def __repr__(self):
        return f"Program({len(self.statements)} statements)"
