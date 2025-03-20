
# #!/usr/bin/env python3
# import sys
# from parser_module import generate_ir
# from semantic_module import semantic_check
# from optimization_module import constant_folding
# from codegen_module import generate_target_code

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python compiler.py <source_file>")
#         sys.exit(1)

#     source_file = sys.argv[1]
#     try:
#         with open(source_file, "r") as f:
#             source_code = f.read()
#     except Exception as e:
#         print(f"Error reading file '{source_file}': {e}")
#         sys.exit(1)

#     print("Source Code:")
#     print("-" * 40)
#     print(source_code)
#     print("-" * 40)

#     # Generate IR from the source code.
#     ir_result, final_result = generate_ir(source_code)
#     print("Initial IR Code:")
#     for line in ir_result:
#         print(line)
#     print(f"Final Result Variable: {final_result}")

#     # Perform semantic analysis.
#     errors = semantic_check(ir_result)
#     if errors:
#         print("Semantic Errors:")
#         for error in errors:
#             print(error)
#         sys.exit(1)

#     # Optimize the IR.
#     optimized_ir = constant_folding(ir_result)
#     print("\nOptimized IR Code:")
#     for line in optimized_ir:
#         print(line)

#     # Generate target pseudo-assembly code.
#     target_code = generate_target_code(optimized_ir)
#     print("\nTarget Code (Pseudo-Assembly):")
#     for line in target_code:
#         print(line)
#     print("\n" + "-" * 40 + "\n")

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
# import sys
# from parser_module import generate_ir
# from semantic_module import semantic_check
# from optimization_module import constant_folding
# from codegen_module import generate_target_code

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python compiler.py <source_file>")
#         sys.exit(1)

#     source_file = sys.argv[1]
#     try:
#         with open(source_file, "r") as f:
#             source_code = f.read()
#     except Exception as e:
#         print(f"Error reading file '{source_file}': {e}")
#         sys.exit(1)

#     print("Source Code:")
#     print("-" * 40)
#     print(source_code)
#     print("-" * 40)

#     # Generate IR from the source code.
#     ir_result, final_result = generate_ir(source_code)
#     print("Initial IR Code:")
#     for line in ir_result:
#         print(line)
#     print(f"Final Result Variable: {final_result}")

#     # Perform semantic analysis.
#     errors = semantic_check(ir_result)
#     if errors:
#         print("Semantic Errors:")
#         for error in errors:
#             print(error)
#         sys.exit(1)

#     # Optimize the IR.
#     optimized_ir = constant_folding(ir_result)
#     print("\nOptimized IR Code:")
#     for line in optimized_ir:
#         print(line)

#     # Generate target pseudo-assembly code.
#     target_code = generate_target_code(optimized_ir)
#     print("\nTarget Code (Pseudo-Assembly):")
#     for line in target_code:
#         print(line)
#     print("\n" + "-" * 40 + "\n")

# if __name__ == "__main__":
#     main()



#!/usr/bin/env python3
import sys
from parser_module import generate_ir, variables
from semantic_module import semantic_check
from optimization_module import constant_folding
from codegen_module import generate_target_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        with open(source_file, "r") as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file '{source_file}': {e}")
        sys.exit(1)

    print("Source Code:")
    print("-" * 40)
    print(source_code)
    print("-" * 40)

    # Generate IR from the source code.
    ir_result, final_result = generate_ir(source_code)
    print("Initial IR Code:")
    for line in ir_result:
        print(line)
    print(f"Final Result Variable: {final_result}")

    # Perform semantic analysis.
    errors = semantic_check(ir_result)
    if errors:
        print("Semantic Errors:")
        for error in errors:
            print(error)
        sys.exit(1)

    # Optimize the IR.
    optimized_ir = constant_folding(ir_result)
    print("\nOptimized IR Code:")
    for line in optimized_ir:
        print(line)

    # Generate target pseudo-assembly code.
    target_code = generate_target_code(optimized_ir)
    print("\nTarget Code (Pseudo-Assembly):")
    for line in target_code:
        print(line)
    
    # Print the computed result for variable 'b', if defined.
    # if "b" in variables:
    #     print("\nRESULT:", variables["b"])

    # Instead of printing "b", print "d" (or the last assigned variable)
    if "d" in variables:
        print("\nRESULT:", variables["d"])
    elif len(variables) > 0:
        last_var = list(variables.keys())[-1]  # Get the last assigned variable
    print("\nRESULT:", variables[last_var])


    print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    main()
