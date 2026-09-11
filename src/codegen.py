"""Python code generator from AST."""

from src.ast import (
    Assignment,
    ASTNode,
    BinaryOp,
    ForLoop,
    Identifier,
    IfStatement,
    InputStatement,
    ListLiteral,
    Literal,
    PrintStatement,
    Program,
    RepeatLoop,
    UnaryOp,
    VariableDeclaration,
    WhileLoop,
)


class CodeGenerator:
    """Generates Python code from AST nodes."""

    def __init__(self):
        self.indent_level = 0
        self.indent_string = "    "

    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1

    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)

    def get_indent(self) -> str:
        """Get the current indentation string."""
        return self.indent_string * self.indent_level

    def generate(self, node: ASTNode) -> str:
        """Generate Python code from an AST node."""
        return node.accept(self)

    def visit_program(self, node: Program) -> str:
        """Generate code for a program."""
        lines = []
        for stmt in node.statements:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        return "\n".join(lines)

    def visit_variable_declaration(self, node: VariableDeclaration) -> str:
        """Generate code for a variable declaration."""
        value_code = self.generate(node.value)

        if node.var_type:
            type_hint = self._python_type(node.var_type)
            return f"{node.name}: {type_hint} = {value_code}"
        else:
            return f"{node.name} = {value_code}"

    def visit_assignment(self, node: Assignment) -> str:
        """Generate code for an assignment."""
        value_code = self.generate(node.value)
        return f"{node.name} = {value_code}"

    def visit_for_loop(self, node: ForLoop) -> str:
        """Generate code for a for loop."""
        iterable_code = self.generate(node.iterable)
        lines = [f"for {node.item_var} in {iterable_code}:"]

        self.indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code:
                lines.append(self.get_indent() + stmt_code)
        self.dedent()

        return "\n".join(lines)

    def visit_while_loop(self, node: WhileLoop) -> str:
        """Generate code for a while loop."""
        condition_code = self.generate(node.condition)
        lines = [f"while {condition_code}:"]

        self.indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code:
                lines.append(self.get_indent() + stmt_code)
        self.dedent()

        return "\n".join(lines)

    def visit_repeat_loop(self, node: RepeatLoop) -> str:
        """Generate code for a repeat loop."""
        count_code = self.generate(node.count)
        lines = [f"for _ in range({count_code}):"]

        self.indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code:
                lines.append(self.get_indent() + stmt_code)
        self.dedent()

        return "\n".join(lines)

    def visit_if_statement(self, node: IfStatement) -> str:
        """Generate code for an if/else statement."""
        lines = [f"if {self.generate(node.condition)}:"]
        self.indent()
        if node.then_body:
            for stmt in node.then_body:
                stmt_code = self.generate(stmt)
                if stmt_code:
                    lines.append(self.get_indent() + stmt_code)
        else:
            lines.append(self.get_indent() + "pass")
        self.dedent()
        if node.else_body:
            lines.append("else:")
            self.indent()
            for stmt in node.else_body:
                stmt_code = self.generate(stmt)
                if stmt_code:
                    lines.append(self.get_indent() + stmt_code)
            self.dedent()
        return "\n".join(lines)

    def visit_print_statement(self, node: PrintStatement) -> str:
        """Generate code for a print statement."""
        return f"print({self.generate(node.expression)})"

    def visit_input_statement(self, node: InputStatement) -> str:
        """Generate code for a user input statement."""
        if node.prompt is not None:
            return f"{node.name} = input({self.generate(node.prompt)})"
        return f"{node.name} = input()"

    def visit_literal(self, node: Literal) -> str:
        """Generate code for a literal."""
        if isinstance(node.value, str):
            return repr(node.value)
        elif isinstance(node.value, bool):
            return "True" if node.value else "False"
        elif isinstance(node.value, (int, float)):
            return str(node.value)
        else:
            return repr(node.value)

    def visit_list_literal(self, node: ListLiteral) -> str:
        """Generate code for a list literal."""
        elements = [self.generate(elem) for elem in node.elements]
        return "[" + ", ".join(elements) + "]"

    def visit_identifier(self, node: Identifier) -> str:
        """Generate code for an identifier."""
        return node.name

    def visit_binary_op(self, node: BinaryOp) -> str:
        """Generate code for a binary operation."""
        left_code = self.generate(node.left)
        right_code = self.generate(node.right)

        op_map = {
            "and": "and",
            "or": "or",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
        }

        op = op_map.get(node.operator, node.operator)

        return f"{left_code} {op} {right_code}"

    def visit_unary_op(self, node: UnaryOp) -> str:
        """Generate code for a unary operation."""
        operand_code = self.generate(node.operand)

        if node.operator == "not":
            return f"not {operand_code}"
        elif node.operator == "-":
            return f"-{operand_code}"
        else:
            return f"{node.operator}{operand_code}"

    def _python_type(self, type_name: str) -> str:
        """Convert natural language type to Python type hint."""
        type_map = {
            "inteiro": "int",
            "int": "int",
            "numero": "float",
            "float": "float",
            "texto": "str",
            "str": "str",
            "booleano": "bool",
            "bool": "bool",
            "lista": "list",
        }
        return type_map.get(type_name.lower(), "Any")
