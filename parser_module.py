# parser_module.py
import math
import ply.yacc as yacc
from lexer_module import tokens, lexer

# Global counters and storage.
temp_counter = 0
label_counter = 0
ir_code = []       # List to store IR instructions.
variables = {}     # For assignments.
symbol_table = {}  # Stores variable name, type, and value

def new_temp():
    global temp_counter
    temp_name = f't{temp_counter}'
    temp_counter += 1
    return temp_name

def new_label():
    global label_counter
    label_name = f'L{label_counter}'
    label_counter += 1
    return label_name

# -------------------------
# Grammar rules for a program
# -------------------------

def p_program_single(p):
    'program : statement'
    p[0] = None

def p_program_newline(p):
    'program : program NEWLINE statement'
    p[0] = None

def p_program_semicolon(p):
    'program : program SEMICOLON statement'
    p[0] = None

# -------------------------
# Statement rules
# -------------------------

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]

# def p_statement_assign(p):
#     'statement : IDENTIFIER ASSIGN expression'
#     variables[p[1]] = p[3]
#     ir_code.append(f'{p[1]} = {p[3]}')
#     p[0] = p[1]

# def p_statement_assign(p):
#     'statement : IDENTIFIER ASSIGN expression'
#     variables[p[1]] = p[3]  # p[3] now holds an int (if possible)
#     ir_code.append(f'{p[1]} = {p[3]}')
#     p[0] = p[1]


def p_statement_assign(p):
    'statement : IDENTIFIER ASSIGN expression'
    
    # Determine the data type of the assigned value
    value = p[3]
    var_type = "int" if isinstance(value, int) else "string"
    
    # Store in symbol table
    symbol_table[p[1]] = {"type": var_type, "value": value}
    
    # Generate IR code
    ir_code.append(f'{p[1]} = {value}')
    
    p[0] = p[1]


def p_statement_array_assign(p):
    'statement : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'
    ir_code.append(f'{p[1]}[{p[3]}] = {p[6]}')
    p[0] = f'{p[1]}[{p[3]}]'

# def p_statement_print(p):
#     '''statement : PRINT LPAREN expression RPAREN
#                  | PRINT LPAREN STRING RPAREN'''
#     if isinstance(p[3], str):
#         line = f'print "{p[3]}"'
#     else:
#         line = f'print {p[3]}'
#     ir_code.append(line)
#     p[0] = line

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN
                 | PRINT LPAREN STRING RPAREN'''
    if isinstance(p[3], str):
        line = f'print "{p[3]}"'
    else:
        line = f'print {p[3]}'  # p[3] is the computed value (e.g., 22)
    ir_code.append(line)
    p[0] = line



def p_statement_if_else(p):
    'statement : IF LPAREN expression RPAREN statement ELSE statement'
    false_label = new_label()
    end_label = new_label()
    ir_code.append(f'if not {p[3]} goto {false_label}')
    ir_code.append(f'{p[5]}')
    ir_code.append(f'goto {end_label}')
    ir_code.append(f'{false_label}:')
    ir_code.append(f'{p[7]}')
    ir_code.append(f'{end_label}:')
    p[0] = "if-else statement"

# def p_statement_if(p):
#     'statement : IF LPAREN expression RPAREN statement'
#     false_label = new_label()
#     ir_code.append(f'if not {p[3]} goto {false_label}')
#     ir_code.append(f'{p[5]}')
#     ir_code.append(f'{false_label}:')
#     p[0] = "if statement"


def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN statement'
    false_label = new_label()
    end_label = new_label()

    cond_var = new_temp()
    ir_code.append(f'{cond_var} = {p[3]}')  # Store condition result

    ir_code.append(f'if not {cond_var} goto {false_label}')
    ir_code.append(f'{p[5]}')  # Execute if block
    ir_code.append(f'goto {end_label}')

    ir_code.append(f'{false_label}:')
    ir_code.append(f'{end_label}:')
    p[0] = "if statement"


# def p_statement_for(p):
#     'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
#     start_label = new_label()
#     exit_label = new_label()
#     # Initialization.
#     ir_code.append(f'{p[3]}')
#     ir_code.append(f'{start_label}:')
#     # Condition check.
#     ir_code.append(f'if not {p[5]} goto {exit_label}')
#     # Loop body.
#     ir_code.append(f'{p[9]}')
#     # Post (update).
#     ir_code.append(f'{p[7]}')
#     ir_code.append(f'goto {start_label}')
#     ir_code.append(f'{exit_label}:')
#     p[0] = "for loop"
# def p_statement_for(p):
#     'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
#     start_label = new_label()
#     exit_label = new_label()
    
#     # Initialization
#     ir_code.append(f'{p[3]}')
    
#     # Loop start
#     ir_code.append(f'{start_label}:')
    
#     # Condition check
#     cond_var = new_temp()
#     ir_code.append(f'{cond_var} = {p[5]}')  # Store condition result
#     ir_code.append(f'if not {cond_var} goto {exit_label}')
    
#     # Loop body
#     ir_code.append(f'{p[9]}')
    
#     # Increment (update)
#     ir_code.append(f'{p[7]}')
    
#     # Jump back to condition check
#     ir_code.append(f'goto {start_label}')
    
#     # Exit label
#     ir_code.append(f'{exit_label}:')
#     p[0] = "for loop"


def p_statement_for(p):
    'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
    start_label = new_label()
    exit_label = new_label()

    # Initialization
    ir_code.append(f'{p[3]}')  

    # Loop condition check
    ir_code.append(f'{start_label}:')
    cond_var = new_temp()
    ir_code.append(f'{cond_var} = {p[5]}')  # Condition check
    ir_code.append(f'if not {cond_var} goto {exit_label}')

    # Loop body
    ir_code.append(f'{p[9]}')  

    # Increment step
    ir_code.append(f'{p[7]}')

    # Jump back to condition check
    ir_code.append(f'goto {start_label}')
    
    # Exit loop
    ir_code.append(f'{exit_label}:')
    p[0] = "for loop"


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN statement'
    start_label = new_label()
    exit_label = new_label()
    ir_code.append(f'{start_label}:')
    ir_code.append(f'if not {p[3]} goto {exit_label}')
    ir_code.append(f'{p[5]}')
    ir_code.append(f'goto {start_label}')
    ir_code.append(f'{exit_label}:')
    p[0] = "while loop"

# -------------------------
# Expression rules
# -------------------------

# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression
#                   | expression MOD expression'''
#     temp_var = new_temp()
#     if p[2] == '%':
#         ir_code.append(f'{temp_var} = {p[1]} % {p[3]}')
#     else:
#         ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
#     p[0] = temp_var


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    # If both operands are integers, compute the result
    if isinstance(p[1], int) and isinstance(p[3], int):
        if p[2] == '+':
            result = p[1] + p[3]
        elif p[2] == '-':
            result = p[1] - p[3]
        elif p[2] == '*':
            result = p[1] * p[3]
        elif p[2] == '/':
            result = p[1] // p[3]  # Integer division
        elif p[2] == '%':
            result = p[1] % p[3]
        temp_var = new_temp()
        ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
        p[0] = result
    else:
        temp_var = new_temp()
        ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
        p[0] = temp_var




def p_expression_relational(p):
    'expression : expression LT expression'
    temp_var = new_temp()
    ir_code.append(f'{temp_var} = {p[1]} < {p[3]}')
    p[0] = temp_var

def p_expression_array_access(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    temp_var = new_temp()
    ir_code.append(f'{temp_var} = {p[1]}[{p[3]}]')
    p[0] = temp_var

# def p_expression_number(p):
#     'expression : NUMBER'
#     p[0] = str(p[1])


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]  # Return the number as an integer


# def p_expression_identifier(p):
#     'expression : IDENTIFIER'
#     if p[1] in variables:
#         p[0] = variables[p[1]]
#     else:
#         # Return the identifier as a literal (for use in conditions).
#         p[0] = p[1]

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    if p[1] in symbol_table:
        p[0] = symbol_table[p[1]]["value"]  # Fetch stored value
    else:
        print(f"Error: Undefined variable '{p[1]}'")
        p[0] = 0  # Default value



def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_trig(p):
    '''expression : SIN LPAREN expression RPAREN
                  | COS LPAREN expression RPAREN
                  | TAN LPAREN expression RPAREN
                  | COSEC LPAREN expression RPAREN
                  | SEC LPAREN expression RPAREN
                  | COT LPAREN expression RPAREN'''
    func_name = p[1].lower()
    temp_var = new_temp()
    ir_code.append(f'{temp_var} = {func_name}(math.radians({p[3]}))')
    p[0] = temp_var

def p_expression_comparison(p):
    'expression : expression EQUALS expression'
    temp_var = new_temp()
    ir_code.append(f'{temp_var} = {p[1]} == {p[3]}')
    p[0] = temp_var

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error")

# Build the parser with the start symbol "program".
parser = yacc.yacc(start='program')

# def generate_ir(source_code):
#     global ir_code, temp_counter, label_counter
#     ir_code = []          # Reset IR storage.
#     temp_counter = 0      # Reset temporary variable counter.
#     label_counter = 0     # Reset label counter.
#     result = parser.parse(source_code, lexer=lexer)
#     return ir_code, result

def generate_ir(source_code):
    global ir_code, temp_counter, label_counter
    ir_code = []          # Reset IR storage.
    temp_counter = 0      # Reset temporary variable counter.
    label_counter = 0     # Reset label counter.
    result = parser.parse(source_code, lexer=lexer)

    # Print Symbol Table
    print("\nSymbol Table:")
    for var, details in symbol_table.items():
        print(f"{var}: Type={details['type']}, Value={details['value']}")

    return ir_code, result



if __name__ == "__main__":
    # For testing purposes, run the REPL.
    while True:
        expr = input("Parser> ")
        if expr == "-1":
            break
        ir, res = generate_ir(expr)
        print("IR:")
        for line in ir:
            print(line)
        print("Result:", res)
