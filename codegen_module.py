# codegen_module.py
import re

def generate_target_code(ir_lines):
    """
    Translate the IR (three-address code) into pseudo-assembly code.
    """
    target_code = []
    for line in ir_lines:
        # Process assignment lines, including array element assignments.
        if re.match(r'^[a-zA-Z_]\w*(\[[^\]]+\])?\s*=\s*.+$', line):
            # If the line contains an array element (e.g., a[3] = 5), output directly.
            if '[' in line and ']' in line:
                target_code.append(line)
            else:
                parts = line.split('=')
                lhs = parts[0].strip()
                rhs = parts[1].strip()
                # Check for arithmetic or relational operators.
                if any(op in rhs for op in ['+', '-', '*', '/', '<', '%']):
                    match = re.match(r'(.+)\s*([\+\-\*/<%])\s*(.+)', rhs)
                    if match:
                        op1, operator, op2 = match.groups()
                        if operator == '<':
                            target_code.append(f'; RELATIONAL: {lhs} = {op1.strip()} {operator} {op2.strip()}')
                            target_code.append(f'MOV {lhs}, {op1.strip()}')  # Simplified handling.
                        elif operator == '%':
                            target_code.append(f'MOV {lhs}, {op1.strip()}')
                            target_code.append(f'MOD {lhs}, {op2.strip()}')
                        else:
                            target_code.append(f'MOV {lhs}, {op1.strip()}')
                            if operator == '+':
                                target_code.append(f'ADD {lhs}, {op2.strip()}')
                            elif operator == '-':
                                target_code.append(f'SUB {lhs}, {op2.strip()}')
                            elif operator == '*':
                                target_code.append(f'MUL {lhs}, {op2.strip()}')
                            elif operator == '/':
                                target_code.append(f'DIV {lhs}, {op2.strip()}')
                    else:
                        target_code.append(f'MOV {lhs}, {rhs}')
                else:
                    target_code.append(f'MOV {lhs}, {rhs}')
        # Process print statements.
        elif line.startswith('print'):
            m = re.match(r'print\s+"(.*)"', line)
            if m:
                target_code.append(f'PRINT_STRING {m.group(1)}')
            else:
                parts = line.split()
                if len(parts) >= 2:
                    target_code.append(f'PRINT_VAR {parts[1]}')
        # Process conditional jumps.
        elif line.startswith('if not'):
            m = re.match(r'if not (.+) goto (.+)', line)
            if m:
                var, label = m.groups()
                target_code.append(f'CMP {var.strip()}, 0')
                target_code.append(f'JE {label.strip()}')
        # Process unconditional goto.
        elif line.startswith('goto'):
            m = re.match(r'goto (.+)', line)
            if m:
                target_code.append(f'JMP {m.group(1).strip()}')
        # Process labels.
        elif re.match(r'^L\d+:', line):
            target_code.append(line)
        else:
            target_code.append(f'; {line}')
    return target_code

if __name__ == "__main__":
    sample_ir = [
        't0 = 2 + 3',
        'print t0',
        'a[3] = 5'
    ]
    target = generate_target_code(sample_ir)
    for line in target:
        print(line)
