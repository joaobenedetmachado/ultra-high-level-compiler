"""Tests for example UHL files."""

from pathlib import Path

from src.compiler import Compiler


def test_basic_uhl():
    """Test that basic.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "basic.uhl"))

    expected = """x = 5.0
name: str = 'Hello, World!'
is_active: bool = True
x = 10.0
name = 'Python'"""

    assert actual.strip() == expected.strip()


def test_loops_uhl():
    """Test that loops.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "loops.uhl"))

    expected = """numbers = [1, 2, 3, 4, 5]
for number in numbers:
    squared = number * number
    squared = squared + 1
    counter = 0.0
    while counter < 10:
        counter = counter + 1
        for _ in range(5):
            message = 'Iteration'
            message = message"""

    assert actual.strip() == expected.strip()


def test_operators_uhl():
    """Test that operators.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "operators.uhl"))

    expected = """a = 10.0
b = 5.0
sum = a + b
product = a * b
difference = a - b
quotient = a / b
is_greater = a > b
is_equal = a == b
result = a + b * 2
condition = a > 5 and b < 10"""

    assert actual.strip() == expected.strip()


def test_complete_uhl():
    """Test that complete.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "complete.uhl"))

    expected = """total: int = 0
numbers: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for number in numbers:
    total = total + number
    average = total / 10
    count = 0.0
    while count < 5:
        count = count + 1.0
        message = 'Count is'
        message = message
        for _ in range(3):
            iteration = 'Processing'
            iteration = iteration
            is_done: bool = total > 50
            final_result = average * 2 + 10"""

    assert actual.strip() == expected.strip()
