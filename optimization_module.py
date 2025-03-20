# # optimization_module.py
# import re

# def constant_folding(ir_lines):
#     """
#     Perform constant folding on IR lines.
#     If an assignment is of the form "tX = <number> <op> <number>",
#     compute the result and replace the line.
#     """
#     optimized = []
#     for line in ir_lines:
#         match = re.match(r'^(t\d+)\s*=\s*(\d+)\s*([\+\-\*/])\s*(\d+)$', line)
#         if match:
#             temp, num1, operator, num2 = match.groups()
#             num1 = int(num1)
#             num2 = int(num2)
#             result = None
#             if operator == '+':
#                 result = num1 + num2
#             elif operator == '-':
#                 result = num1 - num2
#             elif operator == '*':
#                 result = num1 * num2
#             elif operator == '/':
#                 result = num1 // num2  # integer division for simplicity
#             optimized.append(f'{temp} = {result}')
#         else:
#             optimized.append(line)
#     return optimized

# if __name__ == "__main__":
#     sample_ir = ["t0 = 2 + 3", "x = 4"]
#     opt = constant_folding(sample_ir)
#     for line in opt:
#         print(line)


# optimization_module.py
import re

def constant_folding(ir_lines):
    """
    Perform constant folding on IR lines.
    If an assignment is of the form "tX = <number> <op> <number>",
    compute the result and replace the line.
    """
    optimized = []
    for line in ir_lines:
        match = re.match(r'^(t\d+)\s*=\s*(\d+)\s*([\+\-\*/])\s*(\d+)$', line)
        if match:
            temp, num1, operator, num2 = match.groups()
            num1 = int(num1)
            num2 = int(num2)
            result = None
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 // num2  # integer division for simplicity
            optimized.append(f'{temp} = {result}')
        else:
            optimized.append(line)
    return optimized

if __name__ == "__main__":
    sample_ir = ["t0 = 2 + 3", "x = 4"]
    opt = constant_folding(sample_ir)
    for line in opt:
        print(line)
