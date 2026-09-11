"""Parser for natural language constructs."""

from typing import List, Optional, Set

from src.ast import (
    Assignment,
    BinaryOp,
    Expression,
    ForLoop,
    Identifier,
    IfStatement,
    InputStatement,
    ListLiteral,
    Literal,
    PrintStatement,
    Program,
    RepeatLoop,
    Statement,
    UnaryOp,
    VariableDeclaration,
    WhileLoop,
)
from src.lexer import Token, TokenType, fold_word


CREATE_VERBS = {"crie", "criar", "criando"}
DECLARE_VERBS = {"declare", "declarar", "declarando"}
DEFINE_VERBS = {"defina", "definir", "definindo"}
REPEAT_VERBS = {"repita", "repetir", "repetindo"}
PRINT_VERBS = {
    "mostre",
    "mostrar",
    "mostrando",
    "exiba",
    "exibir",
    "exibindo",
    "escreva",
    "escrever",
    "escrevendo",
}
INPUT_VERBS = {"pergunte", "perguntar", "perguntando"}
SAVE_VERBS = {"salve", "salvar", "salvando"}
TYPE_NAMES = {"inteiro", "texto", "numero", "booleano", "lista"}
IS_WORDS = {"eh"}
BOOL_TRUE = {"verdadeiro", "verdadeira"}
BOOL_FALSE = {"falso", "falsa"}


def word_of(token: Optional[Token]) -> str:
    """Return the folded form of a token value."""
    if token is None or not token.value:
        return ""
    return fold_word(token.value)


class Parser:
    """Parses tokens into an Abstract Syntax Tree."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def error(self, message: str):
        """Raise a parser error with position information."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            raise SyntaxError(
                f"Erro do parser na linha {token.line}, coluna {token.column}: {message}"
            )
        else:
            raise SyntaxError(f"Erro do parser no fim da entrada: {message}")

    def current_token(self) -> Optional[Token]:
        """Get the current token."""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a token ahead."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def current_word(self) -> str:
        """Folded value of the current token."""
        return word_of(self.current_token())

    def peek_word(self, offset: int = 1) -> str:
        """Folded value of a token ahead."""
        return word_of(self.peek_token(offset))

    def advance(self):
        """Move to the next token."""
        if self.pos < len(self.tokens):
            self.pos += 1

    def expect(self, token_type: TokenType, value: Optional[str] = None):
        """Expect a specific token type and optionally value."""
        token = self.current_token()
        if token is None or token.type != token_type:
            expected = f"{token_type.name}" + (f" with value {value!r}" if value else "")
            self.error(f"Esperado {expected}, recebido {token.type.name if token else 'EOF'}")
        if value is not None and word_of(token) != fold_word(value):
            self.error(f"Esperado {value!r}, recebido {token.value!r}")
        self.advance()
        return token

    def skip_optional(self, token_type: TokenType, value: Optional[str] = None):
        """Skip a token if it matches, otherwise do nothing."""
        token = self.current_token()
        if token and token.type == token_type:
            if value is None or word_of(token) == fold_word(value):
                self.advance()
                return True
        return False

    def skip_optional_word(self, value: str):
        """Skip a keyword or identifier that matches the folded value."""
        token = self.current_token()
        if token and word_of(token) == fold_word(value):
            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER):
                self.advance()
                return True
        return False

    def skip_any_word(self, values: Set[str]) -> bool:
        """Skip the current word if it is in the given folded set."""
        if self.current_word() in values:
            if self.current_token() and self.current_token().type in (
                TokenType.KEYWORD,
                TokenType.IDENTIFIER,
            ):
                self.advance()
                return True
        return False

    def skip_paragraph_breaks(self):
        """Skip paragraph break tokens."""
        while self.current_token() and self.current_token().type == TokenType.PARAGRAPH_BREAK:
            self.advance()

    def skip_narrative_words(self):
        """Skip common narrative/introductory words that don't affect meaning."""
        statement_starters = {
            "crie",
            "criar",
            "criando",
            "declare",
            "declarar",
            "declarando",
            "defina",
            "definir",
            "definindo",
            "para",
            "enquanto",
            "repita",
            "repetir",
            "repetindo",
            "se",
            "senao",
            "mostre",
            "mostrar",
            "mostrando",
            "exiba",
            "exibir",
            "exibindo",
            "escreva",
            "escrever",
            "escrevendo",
            "pergunte",
            "perguntar",
            "perguntando",
        }
        statement_keywords = {
            "variavel",
            "chamada",
            "chamado",
            "nomeada",
            "nomeado",
            "como",
            "ela",
            "ele",
            "ou",
            "nao",
            "em",
            "faca",
            "verdadeiro",
            "verdadeira",
            "falso",
            "falsa",
            "vezes",
            "passa",
            "passe",
            "mais",
            "menos",
            "dividido",
            "maior",
            "menor",
            "igual",
            "diferente",
        }

        base_narrative_words = {
            "vamos",
            "vou",
            "ir",
            "deixar",
            "deixe",
            "comecar",
            "comece",
            "comecando",
            "iniciar",
            "inicie",
            "agora",
            "primeiro",
            "depois",
            "entao",
            "tambem",
            "assim",
            "precisamos",
            "preciso",
            "queremos",
            "quero",
            "precisa",
            "por",
            "fim",
            "me",
            "eu",
            "nos",
            "este",
            "esta",
            "esse",
            "essa",
            "isto",
            "isso",
            "aquele",
            "aquela",
            "quando",
            "onde",
            "qual",
            "quais",
            "algum",
            "alguma",
            "todo",
            "toda",
            "todos",
            "todas",
            "nosso",
            "nossa",
            "meu",
            "minha",
            "seu",
            "sua",
            "fazer",
            "faz",
            "feito",
            "fazendo",
            "coisa",
            "coisas",
            "ponto",
            "aqui",
            "ali",
            "la",
            "calcular",
            "calcula",
            "resultado",
            "usar",
            "usamos",
            "usando",
            "com",
            "sem",
            "ja",
            "ainda",
            "bem",
            "so",
            "ate",
            "cumprimentar",
            "usuario",
            "ativo",
            "saber",
            "algo",
            "tarde",
            "atualizar",
            "nome",
            "partida",
            "vai",
            "trabalhar",
            "trabalhamos",
            "numeros",
            "processar",
            "processando",
            "contador",
            "loop",
            "laco",
            "atraves",
            "acumular",
            "soma",
            "media",
            "valor",
            "tarefa",
            "incrementar",
            "durante",
            "iteracao",
            "alcancamos",
            "limite",
            "final",
            "aplica",
            "transformacao",
            "realizar",
            "contas",
            "juntos",
            "subtracao",
            "divisao",
            "comparar",
            "valores",
            "verificar",
            "igualdade",
            "combinar",
            "operacoes",
            "logicas",
            "ambas",
            "condicoes",
            "atendidas",
            "construir",
            "programa",
            "calcula",
            "estatisticas",
            "partir",
            "manter",
            "acumulada",
            "iterar",
            "adicionar",
            "contar",
            "vez",
            "checar",
            "atingimos",
            "limiar",
            "lista",
            "contem",
            "queremos",
            "outro",
            "outra",
            "pode",
            "podemos",
            "dar",
            "total",
            "ambos",
            "numeros",
            "sera",
            "sao",
            "foi",
            "sendo",
            "tendo",
            "tendo",
            "entao",
            "logo",
            "enfim",
            "finalmente",
            "mais",
            "tarde",
            "preciso",
            "rastrear",
            "se",
            "esteja",
            "propriamente",
            "cumprimentar",
            "usuario",
            "atualizar",
            "ficando",
            "fica",
            "desse",
            "dessa",
            "disso",
            "daquilo",
            "apenas",
            "somente",
            "realmente",
            "basicamente",
            "entao",
            "portanto",
            "pois",
            "porque",
            "quando",
            "enquanto",
            "antes",
            "apos",
            "depois",
            "durante",
            "uma",
            "um",
            "o",
            "os",
            "as",
            "de",
            "do",
            "da",
            "dos",
            "das",
            "que",
            "ser",
            "eh",
        }

        def is_narrative_word(word):
            if word in base_narrative_words:
                return True
            if word in statement_starters:
                return False
            for base in base_narrative_words:
                if word.startswith(base) and len(word) > len(base):
                    return True
            return False

        skipped_any = False

        while self.current_token():
            token = self.current_token()
            word = word_of(token)

            if token.type == TokenType.KEYWORD and word in {"uma", "um"}:
                peek = word_of(self.peek_token())
                if peek == "variavel" or peek in TYPE_NAMES:
                    break
                self.advance()
                skipped_any = True
                continue

            if word == "para":
                if self.peek_word() == "cada":
                    break
                self.advance()
                skipped_any = True
                continue

            if word == "se":
                if self._looks_like_if():
                    break
                self.advance()
                skipped_any = True
                continue

            if word == "enquanto":
                peek = self.peek_word()
                if peek in {"loop", "laco"}:
                    self.advance()
                    skipped_any = True
                    continue
                break

            if token.type == TokenType.KEYWORD and word in statement_starters:
                break
            if token.type == TokenType.IDENTIFIER and word in statement_starters:
                break

            if word == "como":
                peek = self.peek_word()
                if peek in TYPE_NAMES or peek in {"um", "uma"}:
                    break
                self.advance()
                skipped_any = True
                continue

            if word == "cada":
                prev = word_of(self.tokens[self.pos - 1]) if self.pos > 0 else ""
                if prev == "para":
                    break
                self.advance()
                skipped_any = True
                continue

            if word in statement_keywords:
                if word == "faca":
                    is_do_in_loop = False
                    for i in range(max(0, self.pos - 8), self.pos):
                        if word_of(self.tokens[i]) in (
                            "para",
                            "enquanto",
                            "repita",
                            "repetir",
                            "cada",
                        ):
                            is_do_in_loop = True
                            break
                    if is_do_in_loop:
                        break
                    self.advance()
                    skipped_any = True
                    continue
                if word == "mais":
                    peek = self.peek_word()
                    if peek in {"tarde", "para"} or (
                        self.peek_token() and self.peek_token().type == TokenType.IDENTIFIER
                    ):
                        self.advance()
                        skipped_any = True
                        continue
                break

            if token.type == TokenType.IDENTIFIER:
                peek = self.peek_word()
                if peek in {"passa", "passe"}:
                    break
                if peek == "agora":
                    peek2 = self.peek_word(2)
                    if peek2 in {"eh", "e"} or peek2 == "":
                        break

            is_agora_assignment = False
            if word == "agora":
                peek = self.peek_word()
                if peek in {"eh", "e"}:
                    is_agora_assignment = True
                if self.pos > 0 and self.tokens[self.pos - 1].type == TokenType.IDENTIFIER:
                    is_agora_assignment = True

            is_e_in_statement = False
            if word == "e":
                peek = self.peek_word()
                if peek in DEFINE_VERBS or peek in {"maior", "menor", "igual", "diferente"}:
                    is_e_in_statement = True

            is_ser_in_assignment = False
            if word == "ser":
                for i in range(max(0, self.pos - 3), self.pos):
                    if word_of(self.tokens[i]) in {"passa", "passe"}:
                        is_ser_in_assignment = True
                        break

            if (
                (
                    token.type in (TokenType.IDENTIFIER, TokenType.KEYWORD)
                    and is_narrative_word(word)
                    and not is_agora_assignment
                    and not is_e_in_statement
                    and not is_ser_in_assignment
                )
                or (token.type == TokenType.PUNCTUATION and token.value in (",", ".", ";", ":"))
            ):
                self.advance()
                skipped_any = True
            elif skipped_any and token.type == TokenType.IDENTIFIER:
                peek = self.peek_word()
                if peek in {"passa", "passe", "agora"}:
                    break
                self.advance()
                skipped_any = True
            else:
                break

    def parse(self) -> Program:
        """Parse the tokens into a Program AST node."""
        statements = []

        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_paragraph_breaks()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)

        return Program(statements)

    def parse_statement(self) -> Optional[Statement]:
        """Parse a statement."""
        self.skip_paragraph_breaks()
        self.skip_narrative_words()

        token = self.current_token()
        if not token or token.type in (TokenType.EOF, TokenType.PARAGRAPH_BREAK):
            return None

        token_value = word_of(token)

        if token_value in CREATE_VERBS or token_value in DECLARE_VERBS:
            return self.parse_variable_declaration()

        if token_value in DEFINE_VERBS:
            return self.parse_assignment()

        if token_value == "para" and self.peek_word() == "cada":
            return self.parse_for_loop()

        if token_value == "enquanto":
            return self.parse_while_loop()

        if token_value in REPEAT_VERBS:
            return self.parse_repeat_loop()

        if token_value == "se" and self._looks_like_if():
            return self.parse_if_statement()

        if token_value == "senao":
            return None

        if token_value in PRINT_VERBS:
            return self.parse_print_statement()

        if token_value in INPUT_VERBS:
            return self.parse_input_statement()

        if token.type == TokenType.IDENTIFIER:
            peek = self.peek_word()
            if peek in {"passa", "passe"}:
                return self.parse_assignment()
            if peek == "agora":
                return self.parse_assignment()

        if token:
            self.advance()
        return None

    def match_keyword_sequence(self, keywords: List[str]) -> bool:
        """Check if the next tokens match a sequence of keywords."""
        saved_pos = self.pos

        for keyword in keywords:
            token = self.current_token()
            if not token:
                self.pos = saved_pos
                return False
            if token.type not in (TokenType.KEYWORD, TokenType.IDENTIFIER):
                self.pos = saved_pos
                return False
            if word_of(token) != fold_word(keyword):
                self.pos = saved_pos
                return False
            self.advance()

        self.pos = saved_pos
        return True

    def parse_name(self) -> str:
        """Parse a variable name from an identifier or keyword."""
        token = self.current_token()
        if token is None:
            self.error("Esperado identificador para o nome da variavel")
            return ""
        if token.type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self.advance()
            return token.value
        self.error(f"Esperado identificador para o nome da variavel, recebido {token.type.name}")
        return ""

    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse: crie uma variavel chamada X [como TIPO] e defina ela como Y."""
        token_value = self.current_word()
        if token_value in CREATE_VERBS or token_value in DECLARE_VERBS:
            self.advance()

        self.skip_narrative_words()
        self.skip_any_word({"uma", "um"})
        self.expect(TokenType.KEYWORD, "variavel")
        if not self.skip_any_word({"chamada", "chamado", "nomeada", "nomeado"}):
            self.error("Esperado 'chamada' ou 'chamado' depois de 'variavel'")

        name = self.parse_name()

        var_type = None
        if self.skip_optional_word("como"):
            self.skip_any_word({"um", "uma"})
            if self.current_word() in TYPE_NAMES:
                var_type = self.current_word()
                self.advance()

        self.skip_optional_word("e")
        if self.current_word() in DEFINE_VERBS:
            self.advance()
            self.skip_any_word({"ela", "ele"})
            self.skip_optional_word("como")

        value = self.parse_expression()
        return VariableDeclaration(name, value, var_type)

    def parse_assignment(self) -> Assignment:
        """Parse: defina X como Y / X passa a ser Y / X agora e Y."""
        if self.current_word() in DEFINE_VERBS:
            self.advance()
            name = self.parse_name()
            self.skip_optional_word("como")
            value = self.parse_expression()
            return Assignment(name, value)

        name = self.parse_name()
        if self.skip_any_word({"passa", "passe"}):
            self.skip_optional_word("a")
            self.skip_optional_word("ser")
            value = self.parse_expression()
            return Assignment(name, value)

        if self.skip_optional_word("agora"):
            self.skip_any_word({"eh", "e"})
            value = self.parse_expression()
            return Assignment(name, value)

        self.error("Esperado 'passa a ser' ou 'agora e' depois do identificador")

    def parse_for_loop(self) -> ForLoop:
        """Parse: para cada X em Y, faca ..."""
        self.expect(TokenType.KEYWORD, "para")
        self.expect(TokenType.KEYWORD, "cada")

        item_var = self.parse_name()
        self.expect(TokenType.KEYWORD, "em")
        iterable = self.parse_expression()

        self.skip_optional(TokenType.PUNCTUATION, ",")
        self.skip_narrative_words()
        self.skip_optional_word("faca")

        body = self.parse_block()
        return ForLoop(item_var, iterable, body)

    def parse_while_loop(self) -> WhileLoop:
        """Parse: enquanto X, faca ..."""
        self.expect(TokenType.KEYWORD, "enquanto")
        condition = self.parse_expression()

        if self.current_word() in IS_WORDS or (
            self.current_word() == "e" and self.peek_word() in BOOL_TRUE
        ):
            self.advance()
            self.skip_any_word(BOOL_TRUE)

        self.skip_optional(TokenType.PUNCTUATION, ",")
        self.skip_narrative_words()
        self.skip_optional_word("faca")

        body = self.parse_block()
        return WhileLoop(condition, body)

    def parse_repeat_loop(self) -> RepeatLoop:
        """Parse: repita N vezes, faca ..."""
        self.skip_any_word(REPEAT_VERBS)
        count = self.parse_primary()
        self.expect(TokenType.KEYWORD, "vezes")

        self.skip_optional(TokenType.PUNCTUATION, ",")
        self.skip_narrative_words()
        self.skip_optional_word("faca")

        body = self.parse_block()
        return RepeatLoop(count, body)

    def _looks_like_if(self) -> bool:
        """A 'se' is a conditional only when 'entao' starts a real branch."""
        for offset in range(1, 24):
            token = self.peek_token(offset)
            if token is None or token.type in (TokenType.EOF, TokenType.PARAGRAPH_BREAK):
                return False
            word = word_of(token)
            if word == "entao":
                following = word_of(self.peek_token(offset + 1))
                if following in {
                    "vamos",
                    "vou",
                    "crie",
                    "criar",
                    "declare",
                    "declarar",
                    "defina",
                    "definir",
                    "preciso",
                    "queremos",
                    "quero",
                }:
                    return False
                return True
            if word in {
                "crie",
                "criar",
                "declare",
                "defina",
                "para",
                "enquanto",
                "repita",
                "senao",
                "mostre",
                "exiba",
                "escreva",
                "pergunte",
            }:
                return False
        return False

    def parse_if_statement(self) -> IfStatement:
        """Parse: se CONDICAO entao ... senao ..."""
        self.expect(TokenType.KEYWORD, "se")
        condition = self.parse_expression()
        self.skip_optional(TokenType.PUNCTUATION, ",")
        self.skip_optional_word("entao")
        then_body = self.parse_block(stop_keywords={"senao"})
        else_body: List[Statement] = []
        if self.current_word() == "senao":
            self.advance()
            else_body = self.parse_block(stop_at_paragraph=True)
        return IfStatement(condition, then_body, else_body)

    def parse_print_statement(self) -> PrintStatement:
        """Parse: mostre / exiba / escreva EXPR."""
        if not self.skip_any_word(PRINT_VERBS):
            self.error("Esperado 'mostre', 'exiba' ou 'escreva'")
        self.skip_optional_word("o")
        if self.skip_optional_word("valor"):
            self.skip_optional_word("de")
        expression = self.parse_expression()
        return PrintStatement(expression)

    def parse_input_statement(self) -> InputStatement:
        """Parse: pergunte [PROMPT] e salve em NOME."""
        if not self.skip_any_word(INPUT_VERBS):
            self.error("Esperado 'pergunte'")
        prompt = None
        token = self.current_token()
        if token and token.type == TokenType.STRING:
            prompt = Literal(token.value)
            self.advance()
        self.skip_optional_word("e")
        if not self.skip_any_word(SAVE_VERBS):
            self.error("Esperado 'salve' depois de 'pergunte'")
        self.skip_optional_word("em")
        name = self.parse_name()
        return InputStatement(name, prompt)

    def parse_block(
        self, stop_keywords: Optional[Set[str]] = None, stop_at_paragraph: bool = False
    ) -> List[Statement]:
        """Parse a block of statements."""
        stop = set(stop_keywords or [])
        body = []

        self.skip_paragraph_breaks()

        while True:
            token = self.current_token()
            if not token or token.type == TokenType.EOF or token.type == TokenType.PARAGRAPH_BREAK:
                break
            if word_of(token) in stop:
                break

            saved_pos = self.pos
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            elif self.pos == saved_pos:
                break

            if stop_at_paragraph:
                nxt = self.current_token()
                if (
                    nxt is None
                    or nxt.type == TokenType.EOF
                    or nxt.type == TokenType.PARAGRAPH_BREAK
                ):
                    break
            else:
                self.skip_paragraph_breaks()

        return body

    def _statement_keywords(self) -> Set[str]:
        return {
            "crie",
            "criar",
            "criando",
            "declare",
            "declarar",
            "declarando",
            "defina",
            "definir",
            "para",
            "enquanto",
            "repita",
            "repetir",
            "se",
            "entao",
            "senao",
            "cada",
            "mostre",
            "mostrar",
            "exiba",
            "exibir",
            "escreva",
            "escrever",
            "pergunte",
            "perguntar",
        }

    def parse_expression(self) -> Expression:
        """Parse an expression."""
        token = self.current_token()
        if token and word_of(token) in self._statement_keywords():
            self.error(f"Palavra-chave de comando inesperada '{token.value}' - esperada expressao")
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        left = self.parse_logical_and()
        starters = self._statement_keywords()

        while self.current_word() == "ou":
            peek = self.peek_word()
            if peek in starters:
                break
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, "or", right)

        return left

    def parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        left = self.parse_comparison()
        starters = self._statement_keywords()
        narrative_after_e = {
            "por",
            "fim",
            "depois",
            "tambem",
            "assim",
            "vamos",
            "crie",
            "criar",
            "declare",
            "defina",
            "para",
            "enquanto",
            "repita",
            "cada",
            "agora",
            "finalmente",
            "logo",
        }

        while self.current_word() == "e":
            peek = self.peek_word()
            if peek in {"maior", "menor", "igual", "diferente"}:
                break
            if peek in narrative_after_e or peek in starters:
                break
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, "and", right)

        return left

    def _consume_is_word(self) -> bool:
        """Consume é/eh, or unaccented e before a comparison word."""
        word = self.current_word()
        if word in IS_WORDS:
            self.advance()
            return True
        if word == "e" and self.peek_word() in {"maior", "menor", "igual", "diferente"}:
            self.advance()
            return True
        return False

    def parse_comparison(self) -> Expression:
        """Parse comparison expression."""
        left = self.parse_additive()

        while self.current_token():
            token = self.current_token()
            word = word_of(token)

            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER):
                saved = self.pos
                if self._consume_is_word():
                    word = self.current_word()

                if word == "maior":
                    self.advance()
                    self.skip_optional_word("que")
                    right = self.parse_additive()
                    left = BinaryOp(left, ">", right)
                    continue
                if word == "menor":
                    self.advance()
                    self.skip_optional_word("que")
                    right = self.parse_additive()
                    left = BinaryOp(left, "<", right)
                    continue
                if word == "igual":
                    self.advance()
                    self.skip_optional_word("a")
                    right = self.parse_additive()
                    left = BinaryOp(left, "==", right)
                    continue
                if word == "diferente":
                    self.advance()
                    self.skip_optional_word("de")
                    right = self.parse_additive()
                    left = BinaryOp(left, "!=", right)
                    continue

                if self.pos != saved:
                    self.pos = saved
                    break

            if token.type == TokenType.OPERATOR and token.value in (
                "==",
                "!=",
                "<=",
                ">=",
                "<",
                ">",
            ):
                op = token.value
                self.advance()
                right = self.parse_additive()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_additive(self) -> Expression:
        """Parse additive expression (+, -)."""
        left = self.parse_multiplicative()

        while self.current_token():
            token = self.current_token()
            word = word_of(token)

            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER) and word in {
                "mais",
                "menos",
            }:
                op = "+" if word == "mais" else "-"
                self.advance()
                right = self.parse_multiplicative()
                left = BinaryOp(left, op, right)
                continue

            if token.type == TokenType.OPERATOR and token.value in ("+", "-"):
                op = token.value
                self.advance()
                right = self.parse_multiplicative()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_multiplicative(self) -> Expression:
        """Parse multiplicative expression (*, /)."""
        left = self.parse_unary()

        while self.current_token():
            token = self.current_token()
            word = word_of(token)

            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER) and word == "vezes":
                self.advance()
                right = self.parse_unary()
                left = BinaryOp(left, "*", right)
                continue

            if token.type in (TokenType.KEYWORD, TokenType.IDENTIFIER) and word == "dividido":
                self.advance()
                self.skip_optional_word("por")
                right = self.parse_unary()
                left = BinaryOp(left, "/", right)
                continue

            if token.type == TokenType.OPERATOR and token.value in ("*", "/"):
                op = token.value
                self.advance()
                right = self.parse_unary()
                left = BinaryOp(left, op, right)
                continue

            break

        return left

    def parse_unary(self) -> Expression:
        """Parse unary expression."""
        token = self.current_token()
        word = word_of(token)

        if token and word == "nao":
            self.advance()
            operand = self.parse_unary()
            return UnaryOp("not", operand)

        if token and token.type == TokenType.OPERATOR and token.value == "-":
            self.advance()
            operand = self.parse_unary()
            return UnaryOp("-", operand)

        return self.parse_primary()

    def parse_primary(self) -> Expression:
        """Parse primary expression (literals, identifiers, parenthesized)."""
        token = self.current_token()

        if not token:
            self.error("Fim inesperado da entrada")

        starters = self._statement_keywords()
        word = word_of(token)

        if token.type == TokenType.KEYWORD and word in starters:
            self.error(f"Palavra-chave de comando inesperada '{token.value}' na expressao")

        if token.type == TokenType.NUMBER:
            self.advance()
            value = float(token.value) if "." in token.value else int(token.value)
            return Literal(value)

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.KEYWORD and word in BOOL_TRUE:
            self.advance()
            return Literal(True)

        if token.type == TokenType.KEYWORD and word in BOOL_FALSE:
            self.advance()
            return Literal(False)

        if token.type == TokenType.IDENTIFIER:
            if word in starters:
                self.error(f"Palavra-chave de comando inesperada '{token.value}' na expressao")
            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.KEYWORD:
            if word not in starters | {
                "e",
                "ou",
                "nao",
                "em",
                "eh",
                "faca",
                "como",
                "mais",
                "menos",
                "vezes",
                "dividido",
                "passa",
                "passe",
                "agora",
            }:
                self.advance()
                return Identifier(token.value)

        if token.type == TokenType.PUNCTUATION and token.value == "[":
            return self.parse_list_literal()

        if token.type == TokenType.PUNCTUATION and token.value == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.PUNCTUATION, ")")
            return expr

        self.error(f"Token inesperado na expressao: {token.value!r}")

    def parse_list_literal(self) -> Expression:
        """Parse a list literal: [expr1, expr2, ...]"""
        self.expect(TokenType.PUNCTUATION, "[")

        elements = []

        if self.current_token() and self.current_token().value == "]":
            self.advance()
            return ListLiteral([])

        elements.append(self.parse_expression())

        while self.current_token() and self.current_token().value == ",":
            self.advance()
            elements.append(self.parse_expression())

        self.expect(TokenType.PUNCTUATION, "]")
        return ListLiteral(elements)
