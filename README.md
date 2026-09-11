# Ultra High-Level Language (UHL) Compiler

> **Escreva codigo em portugues natural. Compile para Python.**

UHL e uma **linguagem de programacao de altissimo nivel** que permite escrever codigo com sintaxe em portugues, organizado em paragrafos e frases longas. O compilador transforma esse texto em Python limpo e executavel.

## Funcionalidades

- **Sintaxe em linguagem natural**: escreva codigo em frases e paragrafos em portugues
- **Variaveis com tipo opcional**: `inteiro`, `texto`, `numero`, `booleano`, `lista`
- **Lacos intuitivos**: `para cada`, `enquanto` e `repita`
- **Condicionais**: `se` / `entao` / `senao` / `senao se`
- **Funcoes**: `defina uma funcao chamada` com `recebe` e `retorna`
- **Entrada e saida**: `mostre`, `exiba`, `escreva` e `pergunte`
- **Operadores em portugues**: `mais`, `menos`, `vezes`, `dividido por`, `maior que`
- **Estrutura por paragrafos**: organize o codigo como texto corrido
- **Python legivel**: gera codigo formatado e executavel

## Instalacao

### A partir do codigo

```bash
git clone https://github.com/joaobenedetmachado/ultra-high-level-compiler
cd ultra-high-level-compiler
pip install -e .
```

### Uso direto

Nao e obrigatorio instalar. Dá para usar a CLI direto:

```bash
python cli.py entrada.uhl -o saida.py
```

## Inicio rapido

### Exemplo 1: Variaveis

**Entrada** (`examples/basic.uhl`):
```uhl
Vamos comecar. Crie uma variavel chamada x e defina ela como 5.

Agora quero criar uma variavel chamada name como texto e defina ela como "Hello, World!"

x passa a ser 10.
name agora e "Python".
```

**Saida compilada**:
```python
x = 5.0
name: str = 'Hello, World!'
x = 10.0
name = 'Python'
```

### Exemplo 2: Condicionais e saida

**Entrada** (`examples/condicionais.uhl`):
```uhl
Crie uma variavel chamada x e defina ela como 8.

Se x e maior que 3 entao
    mostre "x e grande"
senao
    mostre "x e pequeno"
```

**Saida compilada**:
```python
x = 8.0
if x > 3:
    print('x e grande')
else:
    print('x e pequeno')
```

### Exemplo 3: Entrada do usuario

**Entrada** (`examples/entrada_saida.uhl`):
```uhl
pergunte "Qual seu nome?" e salve em nome
mostre nome
```

**Saida compilada**:
```python
nome = input('Qual seu nome?')
print(nome)
```

## Documentacao da linguagem

### Declaracao de variaveis

```
crie uma variavel chamada <nome> [como <tipo>] e defina ela como <expressao>
declare uma variavel chamada <nome> [como <tipo>] e defina ela como <expressao>
```

**Tipos suportados**:
- `inteiro` → `int`
- `texto` → `str`
- `numero` → `float`
- `booleano` → `bool`
- `lista` → `list`

Acentos sao opcionais: `variavel`/`variável`, `nao`/`não`, `entao`/`então`.

### Atribuicao

```
defina <nome> como <expressao>
<nome> passa a ser <expressao>
<nome> agora e <expressao>
```

### Lacos

```
para cada <item> em <lista> faca
    <comandos>

enquanto <condicao> faca
    <comandos>

repita <n> vezes faca
    <comandos>
```

### Condicional

```
se <condicao> entao
    <comandos>
senao se <condicao> entao
    <comandos>
senao
    <comandos>
```

### Funcoes

```
defina uma funcao chamada <nome> que recebe <a> e <b> e retorna <expressao>
defina uma funcao chamada <nome> que recebe <a>
    <comandos>
    retorna <expressao>

<nome>(<args>)
```

### Entrada e saida

```
mostre <expressao>
exiba <expressao>
escreva o valor de <expressao>
pergunte e salve em <nome>
pergunte "mensagem" e salve em <nome>
```

### Operadores

| Portugues | Simbolo | Exemplo |
|-----------|---------|---------|
| `mais` | `+` | `a mais b` |
| `menos` | `-` | `a menos b` |
| `vezes` | `*` | `a vezes b` |
| `dividido por` | `/` | `a dividido por b` |
| `maior que` | `>` | `a e maior que b` |
| `maior ou igual a` | `>=` | `a e maior ou igual a b` |
| `menor que` | `<` | `a e menor que b` |
| `menor ou igual a` | `<=` | `a e menor ou igual a b` |
| `igual a` | `==` | `a e igual a b` |
| `diferente de` | `!=` | `a e diferente de b` |
| `e` | `and` | `a e maior que 5 e b e menor que 10` |
| `ou` | `or` | `a ou b` |
| `nao` | `not` | `nao ativo` |

Booleanos: `verdadeiro` e `falso`.

## Testes

```bash
pytest tests/
```

Os exemplos em `examples/` sao compilados e comparados com a saida Python esperada, incluindo condicionais e entrada/saida.

## Uso

### Linha de comando

```bash
python cli.py entrada.uhl -o saida.py
python cli.py entrada.uhl
echo "crie uma variavel chamada x e defina ela como 5" | python cli.py -
```

### API em Python

```python
from src.compiler import Compiler

compiler = Compiler()
codigo = compiler.compile("""
crie uma variavel chamada x e defina ela como 5
defina x como x mais 10
mostre x
""")
print(codigo)
```

## Estrutura do projeto

```
.
├── src/
│   ├── ast.py
│   ├── lexer.py
│   ├── parser.py
│   ├── codegen.py
│   └── compiler.py
├── examples/
│   ├── basic.uhl
│   ├── loops.uhl
│   ├── operators.uhl
│   ├── complete.uhl
│   ├── condicionais.uhl
│   ├── entrada_saida.uhl
│   ├── senao_se.uhl
│   └── funcoes.uhl
├── tests/
│   └── test_examples.py
├── cli.py
├── setup.py
└── README.md
```

## Extensibilidade

Para adicionar um novo comando, estenda a AST em `src/ast.py`, o parser em `src/parser.py` e o gerador em `src/codegen.py`.

## Exemplos

Compile qualquer exemplo:

```bash
python cli.py examples/basic.uhl
python cli.py examples/condicionais.uhl
python cli.py examples/entrada_saida.uhl
```
