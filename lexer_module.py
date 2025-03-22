# lexer_module.py
import ply.lex as lex

# List of token names.
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',  # <-- Added MOD here
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'NEWLINE',
    'STRING', 'EQUALS', 'ASSIGN', 'IDENTIFIER', 'LT',
    # Reserved tokens (handled in t_IDENTIFIER)
    'PRINT', 'IF', 'ELSE', 'FOR', 'WHILE',
    'SIN', 'COS', 'TAN', 'COSEC', 'SEC', 'COT'
)

# Reserved words mapping (case-insensitive)
reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'cosec': 'COSEC',
    'sec': 'SEC',
    'cot': 'COT'
}

# Regular expression rules for simple tokens.
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'      # <-- New modulus operator rule
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_EQUALS  = r'=='   # Equality check
t_ASSIGN  = r'='    # Assignment
t_LT      = r'<'    # Less-than operator

t_ignore  = ' \t'

# NEWLINE token: Capture newline characters as statement separators.
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove surrounding quotes
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    data = 'print("Hello, Compiler with arrays!")\nn = 17\n'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
