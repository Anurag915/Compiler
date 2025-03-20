# # # parser_module.py
# # import math
# # import ply.yacc as yacc
# # from lexer_module import tokens, lexer

# # # Global counters and storage.
# # temp_counter = 0
# # label_counter = 0
# # ir_code = []       # List to store IR instructions.
# # variables = {}     # For assignments.

# # def new_temp():
# #     global temp_counter
# #     temp_name = f't{temp_counter}'
# #     temp_counter += 1
# #     return temp_name

# # def new_label():
# #     global label_counter
# #     label_name = f'L{label_counter}'
# #     label_counter += 1
# #     return label_name

# # # -------------------------
# # # Parsing rules
# # # -------------------------

# # def p_statement_expr(p):
# #     'statement : expression'
# #     p[0] = p[1]

# # def p_statement_assign(p):
# #     'statement : IDENTIFIER ASSIGN expression'
# #     # For scalar variable assignment.
# #     variables[p[1]] = p[3]
# #     ir_code.append(f'{p[1]} = {p[3]}')
# #     p[0] = p[1]

# # def p_statement_array_assign(p):
# #     'statement : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'
# #     # For array element assignment.
# #     # Store the value in a special format in the IR.
# #     ir_code.append(f'{p[1]}[{p[3]}] = {p[6]}')
# #     p[0] = f'{p[1]}[{p[3]}]'

# # def p_statement_print(p):
# #     '''statement : PRINT LPAREN expression RPAREN
# #                  | PRINT LPAREN STRING RPAREN'''
# #     if isinstance(p[3], str):
# #         line = f'print "{p[3]}"'
# #     else:
# #         line = f'print {p[3]}'
# #     ir_code.append(line)
# #     p[0] = line

# # def p_statement_if_else(p):
# #     'statement : IF LPAREN expression RPAREN statement ELSE statement'
# #     false_label = new_label()
# #     end_label = new_label()
# #     ir_code.append(f'if not {p[3]} goto {false_label}')
# #     ir_code.append(f'{p[5]}')
# #     ir_code.append(f'goto {end_label}')
# #     ir_code.append(f'{false_label}:')
# #     ir_code.append(f'{p[7]}')
# #     ir_code.append(f'{end_label}:')
# #     p[0] = "if-else statement"

# # def p_statement_for(p):
# #     'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
# #     start_label = new_label()
# #     exit_label = new_label()
# #     # Initialization
# #     ir_code.append(f'{p[3]}')
# #     ir_code.append(f'{start_label}:')
# #     # Condition check
# #     ir_code.append(f'if not {p[5]} goto {exit_label}')
# #     # Loop body
# #     ir_code.append(f'{p[9]}')
# #     # Post (update)
# #     ir_code.append(f'{p[7]}')
# #     ir_code.append(f'goto {start_label}')
# #     ir_code.append(f'{exit_label}:')
# #     p[0] = "for loop"

# # def p_statement_while(p):
# #     'statement : WHILE LPAREN expression RPAREN statement'
# #     start_label = new_label()
# #     exit_label = new_label()
# #     ir_code.append(f'{start_label}:')
# #     ir_code.append(f'if not {p[3]} goto {exit_label}')
# #     ir_code.append(f'{p[5]}')
# #     ir_code.append(f'goto {start_label}')
# #     ir_code.append(f'{exit_label}:')
# #     p[0] = "while loop"

# # def p_expression_binop(p):
# #     '''expression : expression PLUS expression
# #                   | expression MINUS expression
# #                   | expression TIMES expression
# #                   | expression DIVIDE expression'''
# #     temp_var = new_temp()
# #     ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
# #     p[0] = temp_var

# # def p_expression_relational(p):
# #     'expression : expression LT expression'
# #     temp_var = new_temp()
# #     ir_code.append(f'{temp_var} = {p[1]} < {p[3]}')
# #     p[0] = temp_var

# # def p_expression_array_access(p):
# #     'expression : IDENTIFIER LBRACKET expression RBRACKET'
# #     temp_var = new_temp()
# #     # Generate IR for array element access.
# #     ir_code.append(f'{temp_var} = {p[1]}[{p[3]}]')
# #     p[0] = temp_var

# # def p_expression_number(p):
# #     'expression : NUMBER'
# #     p[0] = str(p[1])

# # def p_expression_identifier(p):
# #     'expression : IDENTIFIER'
# #     if p[1] in variables:
# #         p[0] = variables[p[1]]
# #     else:
# #         # For array variables, we might allow them to be used before assignment.
# #         p[0] = p[1]

# # def p_expression_group(p):
# #     'expression : LPAREN expression RPAREN'
# #     p[0] = p[2]

# # def p_expression_trig(p):
# #     '''expression : SIN LPAREN expression RPAREN
# #                   | COS LPAREN expression RPAREN
# #                   | TAN LPAREN expression RPAREN
# #                   | COSEC LPAREN expression RPAREN
# #                   | SEC LPAREN expression RPAREN
# #                   | COT LPAREN expression RPAREN'''
# #     func_name = p[1].lower()  # normalized function name
# #     temp_var = new_temp()
# #     ir_code.append(f'{temp_var} = {func_name}(math.radians({p[3]}))')
# #     p[0] = temp_var

# # def p_expression_comparison(p):
# #     'expression : expression EQUALS expression'
# #     temp_var = new_temp()
# #     ir_code.append(f'{temp_var} = {p[1]} == {p[3]}')
# #     p[0] = temp_var

# # def p_error(p):
# #     if p:
# #         print(f"Syntax error at '{p.value}'")
# #     else:
# #         print("Syntax error")

# # parser = yacc.yacc()

# # def generate_ir(expression):
# #     global ir_code, temp_counter, label_counter
# #     ir_code = []         # Reset IR storage.
# #     temp_counter = 0     # Reset temporary variable counter.
# #     label_counter = 0    # Reset label counter.
# #     result = parser.parse(expression)
# #     return ir_code, result

# # if __name__ == "__main__":
# #     while True:
# #         expr = input("Parser> ")
# #         if expr == "-1":
# #             break
# #         ir, res = generate_ir(expr)
# #         print("IR:")
# #         for line in ir:
# #             print(line)
# #         print("Result:", res)


# # parser_module.py
# import math
# import ply.yacc as yacc
# from lexer_module import tokens, lexer

# # Global counters and storage.
# temp_counter = 0
# label_counter = 0
# ir_code = []       # List to store IR instructions.
# variables = {}     # For assignments.

# def new_temp():
#     global temp_counter
#     temp_name = f't{temp_counter}'
#     temp_counter += 1
#     return temp_name

# def new_label():
#     global label_counter
#     label_name = f'L{label_counter}'
#     label_counter += 1
#     return label_name

# # -------------------------
# # Parsing rules
# # -------------------------

# # Rule for a statement (expression).
# def p_statement_expr(p):
#     'statement : expression'
#     p[0] = p[1]

# # Rule for assignment.
# def p_statement_assign(p):
#     'statement : IDENTIFIER ASSIGN expression'
#     variables[p[1]] = p[3]
#     ir_code.append(f'{p[1]} = {p[3]}')
#     p[0] = p[1]

# # Rule for array element assignment (unchanged).
# def p_statement_array_assign(p):
#     'statement : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'
#     ir_code.append(f'{p[1]}[{p[3]}] = {p[6]}')
#     p[0] = f'{p[1]}[{p[3]}]'

# # Rule for print statement.
# def p_statement_print(p):
#     '''statement : PRINT LPAREN expression RPAREN
#                  | PRINT LPAREN STRING RPAREN'''
#     if isinstance(p[3], str):
#         line = f'print "{p[3]}"'
#     else:
#         line = f'print {p[3]}'
#     ir_code.append(line)
#     p[0] = line

# # Rule for if-else statement.
# def p_statement_if_else(p):
#     'statement : IF LPAREN expression RPAREN statement ELSE statement'
#     false_label = new_label()
#     end_label = new_label()
#     ir_code.append(f'if not {p[3]} goto {false_label}')
#     ir_code.append(f'{p[5]}')
#     ir_code.append(f'goto {end_label}')
#     ir_code.append(f'{false_label}:')
#     ir_code.append(f'{p[7]}')
#     ir_code.append(f'{end_label}:')
#     p[0] = "if-else statement"

# # New rule for if statement without else.
# def p_statement_if(p):
#     'statement : IF LPAREN expression RPAREN statement'
#     false_label = new_label()
#     ir_code.append(f'if not {p[3]} goto {false_label}')
#     ir_code.append(f'{p[5]}')
#     ir_code.append(f'{false_label}:')
#     p[0] = "if statement"

# # Rule for for loop.
# def p_statement_for(p):
#     'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
#     start_label = new_label()
#     exit_label = new_label()
#     ir_code.append(f'{p[3]}')
#     ir_code.append(f'{start_label}:')
#     ir_code.append(f'if not {p[5]} goto {exit_label}')
#     ir_code.append(f'{p[9]}')
#     ir_code.append(f'{p[7]}')
#     ir_code.append(f'goto {start_label}')
#     ir_code.append(f'{exit_label}:')
#     p[0] = "for loop"

# # Rule for while loop.
# def p_statement_while(p):
#     'statement : WHILE LPAREN expression RPAREN statement'
#     start_label = new_label()
#     exit_label = new_label()
#     ir_code.append(f'{start_label}:')
#     ir_code.append(f'if not {p[3]} goto {exit_label}')
#     ir_code.append(f'{p[5]}')
#     ir_code.append(f'goto {start_label}')
#     ir_code.append(f'{exit_label}:')
#     p[0] = "while loop"

# # Rule for binary operations.
# # def p_expression_binop(p):
# #     '''expression : expression PLUS expression
# #                   | expression MINUS expression
# #                   | expression TIMES expression
# #                   | expression DIVIDE expression'''
# #     temp_var = new_temp()
# #     ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
# #     p[0] = temp_var


# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression
#                   | expression MOD expression'''  # <-- Added
#     temp_var = new_temp()
#     if p[2] == '%':
#         ir_code.append(f'{temp_var} = {p[1]} % {p[3]}')
#     else:
#         ir_code.append(f'{temp_var} = {p[1]} {p[2]} {p[3]}')
#     p[0] = temp_var


# # Rule for relational operator (<).
# def p_expression_relational(p):
#     'expression : expression LT expression'
#     temp_var = new_temp()
#     ir_code.append(f'{temp_var} = {p[1]} < {p[3]}')
#     p[0] = temp_var

# # Rule for array element access.
# def p_expression_array_access(p):
#     'expression : IDENTIFIER LBRACKET expression RBRACKET'
#     temp_var = new_temp()
#     ir_code.append(f'{temp_var} = {p[1]}[{p[3]}]')
#     p[0] = temp_var

# # Rule for number.
# def p_expression_number(p):
#     'expression : NUMBER'
#     p[0] = str(p[1])

# # Modified rule for identifier.
# def p_expression_identifier(p):
#     'expression : IDENTIFIER'
#     # Instead of triggering an error, if the variable is undefined, return the identifier as-is.
#     if p[1] in variables:
#         p[0] = variables[p[1]]
#     else:
#         p[0] = p[1]

# # Rule for grouped expression.
# def p_expression_group(p):
#     'expression : LPAREN expression RPAREN'
#     p[0] = p[2]

# # Rule for trigonometric functions.
# def p_expression_trig(p):
#     '''expression : SIN LPAREN expression RPAREN
#                   | COS LPAREN expression RPAREN
#                   | TAN LPAREN expression RPAREN
#                   | COSEC LPAREN expression RPAREN
#                   | SEC LPAREN expression RPAREN
#                   | COT LPAREN expression RPAREN'''
#     func_name = p[1].lower()
#     temp_var = new_temp()
#     ir_code.append(f'{temp_var} = {func_name}(math.radians({p[3]}))')
#     p[0] = temp_var

# # Rule for equality comparison.
# def p_expression_comparison(p):
#     'expression : expression EQUALS expression'
#     temp_var = new_temp()
#     ir_code.append(f'{temp_var} = {p[1]} == {p[3]}')
#     p[0] = temp_var

# def p_error(p):
#     if p:
#         print(f"Syntax error at '{p.value}'")
#     else:
#         print("Syntax error")

# parser = yacc.yacc()

# def generate_ir(expression):
#     global ir_code, temp_counter, label_counter
#     ir_code = []         # Reset IR storage.
#     temp_counter = 0     # Reset temporary variable counter.
#     label_counter = 0    # Reset label counter.
#     result = parser.parse(expression)
#     return ir_code, result

# if __name__ == "__main__":
#     while True:
#         expr = input("Parser> ")
#         if expr == "-1":
#             break
#         ir, res = generate_ir(expr)
#         print("IR:")
#         for line in ir:
#             print(line)
#         print("Result:", res)


# parser_module.py
import math
import ply.yacc as yacc
from lexer_module import tokens, lexer

# Global counters and storage.
temp_counter = 0
label_counter = 0
ir_code = []       # List to store IR instructions.
variables = {}     # For assignments.

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

def p_statement_assign(p):
    'statement : IDENTIFIER ASSIGN expression'
    variables[p[1]] = p[3]
    ir_code.append(f'{p[1]} = {p[3]}')
    p[0] = p[1]

def p_statement_array_assign(p):
    'statement : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'
    ir_code.append(f'{p[1]}[{p[3]}] = {p[6]}')
    p[0] = f'{p[1]}[{p[3]}]'

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN
                 | PRINT LPAREN STRING RPAREN'''
    if isinstance(p[3], str):
        line = f'print "{p[3]}"'
    else:
        line = f'print {p[3]}'
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

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN statement'
    false_label = new_label()
    ir_code.append(f'if not {p[3]} goto {false_label}')
    ir_code.append(f'{p[5]}')
    ir_code.append(f'{false_label}:')
    p[0] = "if statement"

def p_statement_for(p):
    'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN statement'
    start_label = new_label()
    exit_label = new_label()
    # Initialization.
    ir_code.append(f'{p[3]}')
    ir_code.append(f'{start_label}:')
    # Condition check.
    ir_code.append(f'if not {p[5]} goto {exit_label}')
    # Loop body.
    ir_code.append(f'{p[9]}')
    # Post (update).
    ir_code.append(f'{p[7]}')
    ir_code.append(f'goto {start_label}')
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

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    temp_var = new_temp()
    if p[2] == '%':
        ir_code.append(f'{temp_var} = {p[1]} % {p[3]}')
    else:
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

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = str(p[1])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        # Return the identifier as a literal (for use in conditions).
        p[0] = p[1]

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

def generate_ir(source_code):
    global ir_code, temp_counter, label_counter
    ir_code = []          # Reset IR storage.
    temp_counter = 0      # Reset temporary variable counter.
    label_counter = 0     # Reset label counter.
    result = parser.parse(source_code, lexer=lexer)
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
