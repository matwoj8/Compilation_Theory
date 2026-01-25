# Matrix-Oriented Language Interpreter (Python)

## Overview

This project is a complete implementation of an **interpreter for a custom, MATLAB-like programming language**, developed as part of a compiler construction course.  
The language supports **matrix operations, control flow, static type checking, and scoped memory**, and is implemented using classic compiler phases.

The interpreter executes programs **only if parsing and semantic analysis succeed**, closely mirroring the architecture of real-world language implementations.

---

## Language Features

### Data Types
- integers
- floats
- strings
- vectors
- matrices

### Matrix Operations
- matrix creation:
  - `zeros(n)`
  - `ones(n)`
  - `eye(n)`
- matrix literals:
  - `[[1,2,3]; [4,5,6]]`
- element-wise operators:
  - `A .+ B`
  - `A .- B`
  - `A .* B`
  - `A ./ B`
- matrix transpose:
  - `A'`
- MATLAB-style **1-based indexing**:
  - `A[2, 1]`

### Expressions
- binary operators:
  - `+ - * / < <= > >= == !=`
- unary operators:
  - negation (`-`)
  - transpose (`'`)
- assignment operators:
  - `=`
  - `+=`
  - `-=`
  - `*=`
  - `/=`

### Control Flow
- `if / else if / else`
- `while`
- `for i = start:end`
- `break`
- `continue`
- `return`

### Scope & Memory Model
- lexical scoping
- block scopes
- loop scopes
- stack-based runtime memory
- separation of **symbol table** (static analysis) and **runtime memory** (execution)

### Static Type Checking
- variable declaration tracking
- matrix dimension validation
- index bounds checking
- meaningful error messages with line numbers

---

## Architecture

The project follows classical compiler design principles:

- scanner → lexical analysis (SLY)
- parser → syntax analysis + AST construction
- AST → abstract syntax tree representation
- typechecker → semantic analysis
- symboltable → scope-aware symbol management
- interpreter → runtime execution
- memory → stack-based runtime memory
- exceptions → control-flow handling (break / continue / return)

### Visitor Pattern

Both the **TypeChecker** and **Interpreter** are implemented using the **Visitor pattern**, allowing each AST node type to define its own semantic and runtime behavior in a clean and extensible way.

---

## Control Flow Implementation

Non-local control flow (`break`, `continue`, `return`) is implemented using **custom exceptions**, which allows correct behavior even in deeply nested constructs.

- loops catch `BreakException` and `ContinueException`
- functions catch `ReturnValueException`
- scopes are always cleaned up using `try / finally`

This design prevents memory leaks and ensures consistent runtime state.

---

## Example Program

```matlab
A = zeros(7);
B = ones(7);

A[2, 1] = 2.3;
B[6, 6] = 5.5;

C = A .+ B;
print C[2, 1];

m = 2;
n = 10;
print (m + n) > 11;

for i = 1:99 {
    if (i <= 99/16)
        print i;
    else if (i <= 99/8)
        break;
}
```
## How to Run
```bash
python main.py example.m
```

## Execution Pipeline:
- lexical analysis

- parsing and AST construction

- semantic analysis (type checking)

- interpretation (only if no errors are found)

## Error Handling
  The interpreter reports:
- syntax errors

- undeclared variables

- invalid matrix operations

- out-of-bounds indexing

- type mismatches
