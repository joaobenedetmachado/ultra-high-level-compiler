"""Lexer for tokenizing natural language input."""

from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    """Token types for the lexer."""

    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    PARAGRAPH_BREAK = "PARAGRAPH_BREAK"
    EOF = "EOF"


class Token:
    """Represents a token with type, value, and position."""

    def __init__(self, token_type: TokenType, value: str, line: int = 1, column: int = 1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


_ACCENT_TABLE = str.maketrans(
    {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c",
    }
)


def fold_word(word: str) -> str:
    """Lowercase a word and fold accents, keeping é distinct from e."""
    if not word:
        return ""
    lowered = word.lower()
    if lowered == "é":
        return "eh"
    return lowered.translate(_ACCENT_TABLE)


class Lexer:
    """Tokenizes natural language input into tokens."""

    KEYWORDS = {
        "crie",
        "criar",
        "criando",
        "declare",
        "declarar",
        "declarando",
        "uma",
        "um",
        "o",
        "a",
        "os",
        "as",
        "variavel",
        "variável",
        "chamada",
        "chamado",
        "nomeada",
        "nomeado",
        "defina",
        "definir",
        "definindo",
        "ela",
        "ele",
        "como",
        "e",
        "ou",
        "nao",
        "não",
        "para",
        "cada",
        "em",
        "faca",
        "faça",
        "enquanto",
        "eh",
        "é",
        "verdadeiro",
        "verdadeira",
        "falso",
        "falsa",
        "repita",
        "repetir",
        "repetindo",
        "vezes",
        "se",
        "entao",
        "então",
        "senao",
        "senão",
        "mais",
        "menos",
        "dividido",
        "por",
        "maior",
        "que",
        "menor",
        "igual",
        "diferente",
        "de",
        "do",
        "da",
        "dos",
        "das",
        "tipo",
        "inteiro",
        "texto",
        "numero",
        "número",
        "booleano",
        "lista",
        "passa",
        "ser",
        "agora",
    }

    FOLDED_KEYWORDS = {fold_word(word) for word in KEYWORDS}

    OPERATORS = {"+", "-", "*", "/", "==", "!=", "<=", ">=", "<", ">", "e", "ou", "nao"}

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def error(self, message: str):
        """Raise a lexer error with position information."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")

    def current_char(self) -> Optional[str]:
        """Get the current character."""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead."""
        pos = self.pos + offset
        if pos >= len(self.text):
            return None
        return self.text[pos]

    def advance(self):
        """Move to the next character."""
        if self.pos < len(self.text) and self.text[self.pos] == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def skip_comment(self):
        """Skip comment lines (lines starting with #)."""
        if self.current_char() == "#":
            while self.pos < len(self.text) and self.text[self.pos] != "\n":
                self.advance()
            if self.pos < len(self.text):
                self.advance()

    def read_number(self) -> str:
        """Read a number (integer or float)."""
        result = []
        has_dot = False

        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char.isdigit():
                result.append(char)
                self.advance()
            elif char == "." and not has_dot:
                result.append(char)
                has_dot = True
                self.advance()
            else:
                break

        return "".join(result)

    def read_string(self) -> str:
        """Read a string literal."""
        quote_char = self.current_char()
        self.advance()

        result = []
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char == quote_char:
                self.advance()
                break
            elif char == "\\":
                self.advance()
                if self.pos < len(self.text):
                    result.append(self.text[self.pos])
                    self.advance()
            else:
                result.append(char)
                self.advance()
        else:
            self.error("Unterminated string literal")

        return "".join(result)

    def read_identifier_or_keyword(self) -> str:
        """Read an identifier or keyword."""
        result = []

        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char.isalnum() or char == "_":
                result.append(char)
                self.advance()
            else:
                break

        return "".join(result)

    def read_operator(self) -> str:
        """Read an operator."""
        char = self.current_char()

        if self.pos + 1 < len(self.text):
            two_char = char + self.text[self.pos + 1]
            if two_char in ("==", "!=", "<=", ">="):
                self.advance()
                self.advance()
                return two_char

        if char in ("+", "-", "*", "/", "<", ">", "="):
            self.advance()
            return char

        return ""

    def check_paragraph_break(self) -> bool:
        """Check if there's a paragraph break (double newline or empty line)."""
        if self.current_char() == "\n":
            start_pos = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isspace():
                self.advance()

            if self.pos >= len(self.text) or self.text[self.pos] == "\n":
                return True

            self.pos = start_pos
            self.column = 1

        return False

    def tokenize(self) -> List[Token]:
        """Tokenize the input text."""
        self.tokens = []

        while self.pos < len(self.text):
            if self.current_char().isspace():
                if self.check_paragraph_break():
                    self.tokens.append(
                        Token(TokenType.PARAGRAPH_BREAK, "\n\n", self.line, self.column)
                    )
                    continue
                self.skip_whitespace()
                continue

            if self.current_char() == "#":
                self.skip_comment()
                continue

            char = self.current_char()
            start_line = self.line
            start_col = self.column

            if char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, start_line, start_col))
                continue

            if char in ('"', "'"):
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, start_line, start_col))
                continue

            if char.isalpha() or char == "_":
                value = self.read_identifier_or_keyword()
                folded = fold_word(value)
                if folded in self.FOLDED_KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD, folded, start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value, start_line, start_col))
                continue

            if char in ("+", "-", "*", "/", "=", "<", ">", "!"):
                op = self.read_operator()
                if op:
                    self.tokens.append(Token(TokenType.OPERATOR, op, start_line, start_col))
                    continue

            if char in (",", ".", ";", ":", "(", ")", "[", "]", "{", "}"):
                self.tokens.append(Token(TokenType.PUNCTUATION, char, start_line, start_col))
                self.advance()
                continue

            self.error(f"Unexpected character: {char!r}")

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))

        return self.tokens
