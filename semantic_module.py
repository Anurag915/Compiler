# semantic_module.py
def semantic_check(ir_lines):
    """
    Perform a simple semantic analysis on the IR.
    This example checks for any 'error' occurrences in the IR.
    """
    errors = []
    for line in ir_lines:
        if "error" in line:
            errors.append("Semantic error found in IR: " + line)
    return errors

if __name__ == "__main__":
    sample_ir = ["x = error", "t0 = 2 + 3"]
    errs = semantic_check(sample_ir)
    for err in errs:
        print(err)
