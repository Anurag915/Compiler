# 🖥 Basic Compiler - A Simple Interpreter & Code Generator  
# Team Members:
Mr.Anurag Prajapati-122cs0081
Mr.Aman Chourasia-122cs0081

# COMPILER DESIGN @ IIITDM-KURNOOL
## 📌 Overview  
This project is a *basic compiler* that directly executes code using an *interpreter* and generates an *Intermediate Representation (IR)* along with *pseudo-assembly code*. It supports:  
✔ *Loops (for, while)*  
✔ *Conditional Statements (if-else)*  
✔ *Arithmetic Expressions*  
✔ *Print Statements*  

---

## 🚀 Features  
- *Lexical Analysis*: Tokenizes the input code  
- *Syntax Parsing*: Checks for valid syntax  
- *Intermediate Representation (IR)*: Generates IR for optimization  
- *Code Generation*: Produces pseudo-assembly code  
- *Execution*: Interprets the generated code  

---

## 📂 Directory Structure  
📦 BasicCompiler
├── 📂 src # Source code files
│ ├── lexer.py # Lexical analyzer
│ ├── parser.py # Syntax parser
│ ├── ir_gen.py # IR generation
│ ├── codegen.py # Code generator
│ ├── interpreter.py # Execution engine
│ └── main.py # Entry point of the compiler
├── 📂 tests # Test cases
├── 📜 README.md # Documentation
└── 📜 test.py # Sample input file



---

## 🛠 Installation & Usage  
### *🔹 Prerequisites*  
- Python 3.x  
- GCC (if you want to extend for assembly code)  

### *🔹 How to Run*  
```bash
git clone https://github.com/yourusername/BasicCompiler.git
cd BasicCompiler
python3 src/main.py test.py


📝 Sample Code & Output
🔹 Sample Input (test.py)
n = 17
isPrime = 1
for ( i = 2; i < n; i = i + 1 ) 
    if ( n % i == 0 ) isPrime = 0
if ( isPrime == 1 ) print("Prime") else print("Not a prime")

🔹 Expected Output
Prime

🎯 Future Enhancements
✅ Support functions & user-defined variables
✅ Implement error handling & debugging features
✅ Extend to generate real assembly code


🤝 Contributing
Contributions are welcome!

Fork the repository
Create a new branch (feature-branch)
Commit changes and create a pull request

📄 License
This project is licensed under the MIT License.

📞 Contact
📧 Email: anuragprajapati02005@gmail.com
📧 Email: gettoknowaman@gmail.com
🔗 GitHub: https://github.com/Anurag915/Compiler

markdown
Copy
Edit