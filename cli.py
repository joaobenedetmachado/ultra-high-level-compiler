#!/usr/bin/env python3
"""Command-line interface for the ultra high-level language compiler."""

import argparse
import sys
from pathlib import Path

from src.compiler import Compiler


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compila linguagem ultra de alto nivel para Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s entrada.uhl -o saida.py
  %(prog)s entrada.uhl                    # Imprime no stdout
  echo "crie uma variavel chamada x e defina ela como 5" | %(prog)s -
        """,
    )

    parser.add_argument("input", type=str, help='Arquivo de entrada (use "-" para stdin)')

    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Arquivo de saida (padrao: stdout)"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    if args.input == "-":
        source_code = sys.stdin.read()
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Erro: arquivo de entrada '{args.input}' nao encontrado", file=sys.stderr)
            sys.exit(1)

        with open(input_path, encoding="utf-8") as f:
            source_code = f.read()

    compiler = Compiler()
    try:
        python_code = compiler.compile(source_code)
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Erro de compilacao: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"Compilado com sucesso: {args.input} -> {args.output}", file=sys.stderr)
    else:
        print(python_code)


if __name__ == "__main__":
    main()
