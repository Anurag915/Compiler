# main.py
from parser_module import generate_ir
from semantic_module import semantic_check
from optimization_module import constant_folding
from codegen_module import generate_target_code

def main():
    while True:
        expr = input(">>> ")
        if expr == "-1":
            break
        # Generate IR from the source code.
        ir_result, final_result = generate_ir(expr)
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
            continue  # Skip code generation if there are semantic errors.
        
        # Optimize the IR (e.g., constant folding).
        optimized_ir = constant_folding(ir_result)
        print("\nOptimized IR Code:")
        for line in optimized_ir:
            print(line)
        
        # Generate target code (pseudo-assembly) from the optimized IR.
        target_code = generate_target_code(optimized_ir)
        print("\nTarget Code (Pseudo-Assembly):")
        for line in target_code:
            print(line)
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()
