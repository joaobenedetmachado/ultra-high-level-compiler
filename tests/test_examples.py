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


def test_condicionais_uhl():
    """Test that condicionais.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "condicionais.uhl"))

    expected = """x = 8.0
if x > 3:
    print('x e grande')
else:
    print('x e pequeno')
if x == 8:
    print('acertou')"""

    assert actual.strip() == expected.strip()


def test_entrada_saida_uhl():
    """Test that entrada_saida.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "entrada_saida.uhl"))

    expected = """saudacao = 'Ola'
print(saudacao)
print('Bem-vindo')
print(saudacao)
nome = input('Qual seu nome?')
print(nome)
idade = input()
print(idade)"""

    assert actual.strip() == expected.strip()


def test_senao_se_uhl():
    """Test that senao_se.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "senao_se.uhl"))

    expected = """nota = 7.0
if nota >= 7:
    print('aprovado')
elif nota >= 5:
    print('recuperacao')
else:
    print('reprovado')"""

    assert actual.strip() == expected.strip()


def test_funcoes_uhl():
    """Test that funcoes.uhl compiles to expected Python code."""
    compiler = Compiler()
    examples_dir = Path(__file__).parent.parent / "examples"
    actual = compiler.compile_file(str(examples_dir / "funcoes.uhl"))

    expected = """def soma(a, b):
    return a + b
print(soma(2, 3))
def saudar(nome):
    print(nome)
    return nome"""

    assert actual.strip() == expected.strip()
