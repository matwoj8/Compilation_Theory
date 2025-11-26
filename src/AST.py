class Node(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def indentation(self, i):
        print(i * "|\t", end="")

    def accept(self, visitor):
        return visitor.visit(self)


class InstructionsOrEmpty(Node):
    def __init__(self, instructions = None, lineno = None):
        super().__init__(instructions=instructions, lineno=lineno)

class Instructions(Node):
    def __init__(self, instructions, lineno = None):
        super().__init__(instructions = instructions, lineno=lineno)

class BreakStatement(Node):
    def __init__(self, lineno = None):
        super().__init__(lineno = lineno)  

class ContinueStatement(Node):
    def __init__(self, lineno = None):
        super().__init__(lineno = lineno) 

class PrintStatement(Node):
    def __init__(self, printargs, lineno = None):
        super().__init__(printargs = printargs, lineno = lineno)

class BinaryExpression(Node):
    def __init__(self, leftexpr, operator, rightexpr, lineno = None):
        super().__init__(leftexpr = leftexpr, operator = operator, rightexpr = rightexpr, lineno = lineno)

class UnaryExpression(Node):
    def __init__(self, operator, expr, lineno = None):
        super().__init__(operator = operator, expr = expr, lineno = lineno)

class IdTab(Node):
    def __init__(self, id, firstexpr, secondexpr = None, lineno = None):
        super().__init__(id = id, firstexpr = firstexpr, secondexpr = secondexpr, lineno = lineno)

class IntNum(Node):
    def __init__(self, intnum , lineno = None):
        super().__init__(intnum = intnum, lineno = lineno)

class IDNum(Node):
    def __init__(self, id , lineno = None):
        super().__init__(id = id, lineno = lineno)

class StringNum(Node):
    def __init__(self, stringnum , lineno = None):
        super().__init__(stringnum = stringnum, lineno = lineno)

class FloatNum(Node):
    def __init__(self, floatnum , lineno = None):
        super().__init__(floatnum = floatnum, lineno = lineno)

class Matrix(Node):
    def __init__(self, matrix , lineno = None):
        super().__init__(matrix = matrix, lineno = lineno)

class MatFun(Node):
    def __init__(self, function, intnum , lineno = None): #z tego co mi sie wydaje to function to Ones/zeros itd.
        super().__init__(function = function, intnum = intnum, lineno = lineno)

class IfStatement(Node):
    def __init__(self, expr, firstinstruction, secondinstruction = None, lineno = None):
        super().__init__(expr = expr, firstinstruction = firstinstruction, secondinstruction = secondinstruction, lineno = lineno) 

class ReturnStatement(Node):
    def __init__(self, expr = None, lineno = None):
        super().__init__(expr = expr, lineno = lineno)

class WhileLoop(Node):
    def __init__(self, expr, instruction, lineno = None):
        super().__init__(expr = expr, instruction = instruction, lineno = lineno)

class ForLoop(Node):
    def __init__(self, id, firstexpr, secondexpr, instruction, lineno = None):
        super().__init__(id = id, firstexpr = firstexpr, secondexpr = secondexpr, instruction = instruction, lineno = lineno)   

class Assignment(Node):
    def __init__(self, value, operator, expr, lineno = None):
        super().__init__(value = value, operator = operator, expr = expr, lineno = lineno)      

class Error(Node):
    def __init__(self):
        pass