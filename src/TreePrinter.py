import AST

def addToClass(cls):

    def decorator(func):
        # print("DODAJĘ", func.__name__, "DO", cls)
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.InstructionsOrEmpty)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)


    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        if isinstance(self.instructions, list):
            for instr in self.instructions:
                instr.printTree(indent)
        else:
            self.instructions.printTree(indent)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.intnum)

    @addToClass(AST.StringNum)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.stringnum)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.floatnum)

    @addToClass(AST.IDNum)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.id)
    
    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("BREAK")
    
    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("CONTINUE")

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("PRINT")
        if isinstance(self.printargs, list):
            for arg in self.printargs:
                arg.printTree(indent + 1)
        else:
            self.printargs.printTree(indent + 1)

    @addToClass(AST.BinaryExpression)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.operator)
        self.leftexpr.printTree(indent + 1)
        self.rightexpr.printTree(indent + 1)

    @addToClass(AST.UnaryExpression)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.operator)
        self.expr.printTree(indent + 1)

    @addToClass(AST.IdTab)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.id)
        self.firstexpr.printTree(indent + 1)
        if self.secondexpr:
            self.secondexpr.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("MATRIX")
        for row in self.matrix:
            self.indentation(indent + 1)
            print("ROW")
            for elem in row:
                elem.printTree(indent + 2)

    @addToClass(AST.MatFun)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.function)
        self.intnum.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        self.indentation(indent)
        print(self.operator)
        self.value.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("IF")
        self.expr.printTree(indent + 1)
        self.firstinstruction.printTree(indent + 1)
        if self.secondinstruction:
            self.indentation(indent)
            print("ELSE")
            self.secondinstruction.printTree(indent + 1)

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("RETURN")
        if self.expr:
            self.expr.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("FOR")
        self.id.printTree(indent + 1)
        self.firstexpr.printTree(indent + 1)
        self.secondexpr.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        self.indentation(indent)
        print("WHILE")
        self.expr.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    
    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for instr in self.instructions:
            instr.printTree(indent)
    


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body


    # define printTree for other classes
    # ...


