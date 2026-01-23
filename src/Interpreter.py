
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
from AST import *

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        super().__init__()
        self.operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            '>': lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
            '.+' : lambda a, b: self.dotplus(a, b),
            '.-' : lambda a, b: self.dotminus(a, b),
            '.*' : lambda a, b: self.dotmult(a, b),
            './' : lambda a, b: self.dotdiv(a, b),  
        }

    def apply_op(self, op, a, b):
        if isinstance(a, list) and isinstance(b, list):
            if op == '+':
                return self.dotplus(a, b)
            if op == '-':
                return self.dotminus(a, b)
            if op == '*':
                return self.dotmult(a, b)
            if op == '/':
                return self.dotdiv(a, b)

        return self.operations[op](a, b)


    def dotmult(self, A, B):
        if isinstance(A, list) and isinstance(B, list):
            if isinstance(A[0], list) and isinstance(B[0], list):
                # A and B are matrices
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    raise ValueError("Matrices must have the same dimensions for element-wise multiplication.")
                return [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            else:
                # A and B are vectors
                if len(A) != len(B):
                    raise ValueError("Vectors must have the same length for element-wise multiplication.")
                return [A[i] * B[i] for i in range(len(A))]
        else:
            return A * B  # regular multiplication 


    def dotdiv(self, A, B):
        if isinstance(A, list) and isinstance(B, list):
            if isinstance(A[0], list) and isinstance(B[0], list):
                # A and B are matrices
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    raise ValueError("Matrices must have the same dimensions for element-wise division.")
                return [[A[i][j] / B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            else:
                # A and B are vectors
                if len(A) != len(B):
                    raise ValueError("Vectors must have the same length for element-wise division.")
                return [A[i] / B[i] for i in range(len(A))]
        else:
            return A / B  # regular division

    def dotplus(self, A, B):
        if isinstance(A, list) and isinstance(B, list):
            if isinstance(A[0], list) and isinstance(B[0], list):
                # A and B are matrices
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    raise ValueError("Matrices must have the same dimensions for element-wise addition.")
                return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            else:
                # A and B are vectors
                if len(A) != len(B):
                    raise ValueError("Vectors must have the same length for element-wise addition.")
                return [A[i] + B[i] for i in range(len(A))]
        else:
            return A + B  # regular addition

    def dotminus(self, A, B):
        if isinstance(A, list) and isinstance(B, list):
            if isinstance(A[0], list) and isinstance(B[0], list):
                # A and B are matrices
                print(f"debug: Performing element-wise subtraction on matrices of dimensions {len(A)}x{len(A[0])} and {len(B)}x{len(B[0])}")
                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    raise ValueError("Matrices must have the same dimensions for element-wise subtraction.")
                return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            else:
                # A and B are vectors
                if len(A) != len(B):
                    raise ValueError("Vectors must have the same length for element-wise subtraction.")
                return [A[i] - B[i] for i in range(len(A))]
        else:
            return A - B  # regular subtraction



    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node:Instructions):
        for instr in node.instructions:
            instr.accept(self)
    
    @when(AST.InstructionsOrEmpty)
    def visit(self, node):
        self.memory = MemoryStack()
        self.memory.push('global')
        node.instructions.accept(self)

    @when(AST.BinaryExpression)
    def visit(self, node: AST.BinaryExpression):
        r1 = node.leftexpr.accept(self)
        r2 = node.rightexpr.accept(self)
        return self.apply_op(node.operator, r1, r2)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.UnaryExpression)
    def visit(self, node):
        r = node.expr.accept(self)

        if node.operator == 'TRANSPOSE':
            if isinstance(r, list):
                if all(isinstance(row, list) for row in r):
                    # r is a matrix
                    return [list(row) for row in zip(*r)]
                else:
                    # r is a vector
                    return [[elem] for elem in r]
            else:
                return r  # scalar remains unchanged
        else:
            return -r  # UMINUS

    @when(AST.PrintStatement)
    def visit(self, node):
        values = [arg.accept(self) for arg in node.printargs]
        print(*values, sep=' ')

    @when(AST.IdTab)
    def visit(self, node):
        # return the value of the indexed id
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.intnum)
    
    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.floatnum)
    
    @when(AST.StringNum)
    def visit(self, node):
        return str(node.stringnum)
    
    @when(AST.IDNum)
    def visit(self, node):
        return self.memory.get(node.id)

    
    
    @when(AST.BreakStatement)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.ContinueStatement)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.IfStatement)
    def visit(self, node):
        cond = node.expr.accept(self)
        if cond:
            try:
                self.memory.push('if_true')
                if isinstance(node.firstinstruction, list):
                    for instr in node.firstinstruction:
                        instr.accept(self)
                else:
                    node.firstinstruction.accept(self)
            finally:
                self.memory.pop()
        elif node.secondinstruction:
            try:
                self.memory.push('if_false')
                if isinstance(node.secondinstruction, list):
                    for instr in node.secondinstruction:
                        instr.accept(self)
                else:
                    node.secondinstruction.accept(self)
            finally:
                self.memory.pop()
        
    @when(AST.ReturnStatement)
    def visit(self, node):
        value = node.expr.accept(self)
        raise ReturnValueException(value)
    
    @when(AST.MatFun)
    def visit(self, node):
        func = node.function
        arg = node.intnum.accept(self)
        if func == 'zeros':
            return [[0 for _ in range(arg)] for _ in range(arg)]
        elif func == 'ones':
            return [[1 for _ in range(arg)] for _ in range(arg)]
        elif func == 'eye':
            return [[1 if i == j else 0 for j in range(arg)] for i in range(arg)]
        else:
            raise ValueError(f"Unknown matrix function: {func}")

    @when(AST.Matrix)
    def visit(self, node):
        result = []

        for row in node.matrix:
            if isinstance(row, list):
                result.append([elem.accept(self) for elem in row])
            else:
                result.append(row.accept(self))

        return result

    @when(AST.ForLoop)
    def visit(self, node):
        iter_var = node.id
        start = node.firstexpr.accept(self)
        end = node.secondexpr.accept(self)
        self.memory.push('for_loop')
        self.memory.set(iter_var.id, start)
        try:
            while self.memory.get(iter_var.id) <= end:
                if isinstance(node.instruction, list):
                    for instr in node.body.instruction:
                        instr.accept(self)
                else:
                    node.instruction.accept(self)
                self.memory.set(iter_var.id, self.memory.get(iter_var.id) + 1)
        finally:
            self.memory.pop()
    
    @when(AST.WhileLoop)
    def visit(self, node):
        self.memory.push('while_loop')
        try:
            while node.expr.accept(self):
                try:
                    if isinstance(node.instruction, list):
                        for instr in node.instruction.instructions:
                            instr.accept(self)
                    else:
                        node.instruction.accept(self)
                except ContinueException:
                    continue
                except BreakException:
                    break
        finally:
            self.memory.pop()
    
    @when(AST.Block)
    def visit(self, node):
        r = None
        self.memory.push("block")
        try:
            for instr in node.instructions:
                r = instr.accept(self)
        finally:
            self.memory.pop()
        return r
    

    @when(AST.Assignment)
    def visit(self, node):
        if not isinstance(node.value, AST.IdTab):
            name = node.value.id

            if node.operator == '=':
                self.memory.set(name, node.expr.accept(self))
            else:
                print(f"Debug: Performing operation {node.operator[0]} on variable {name}")
                self.memory.set(
                    name,
                    self.apply_op(node.operator[0], self.memory.get(name), node.expr.accept(self))
                )
            return

        tab_name = node.value.id
        matrix = self.memory.get(tab_name)

        i = node.value.firstexpr.accept(self)
        j = node.value.secondexpr.accept(self) if node.value.secondexpr else None

        # MATLAB-like: indeksy od 1
        i -= 1
        if j is not None:
            j -= 1

        if node.operator == '=':
            if j is None:
                matrix[i] = node.expr.accept(self)
            else:
                matrix[i][j] = node.expr.accept(self)
        else:
            if j is None:
                matrix[i] = self.apply_op( node.operator[0], matrix[i], node.expr.accept(self))
            else:
                matrix[i][j] = self.apply_op( node.operator[0], matrix[i][j], node.expr.accept(self))

        self.memory.set(tab_name, matrix)




