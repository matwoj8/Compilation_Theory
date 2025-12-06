#!/usr/bin/python



class NodeVisitor(object):

    def __init__(self):
        self.loop_depth = 0

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.operations = ['=', '+=', '-=', '*=', '/=', '>', '<', '>=', '<=', '==', '!=',
                            '+', '-','.+', '.-', '*', '/', '.*', './']
        self.current_scope = None # todo

    def visit_InstructionOrEmpty(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BreakStatement(self, node):
        if not self.in_loop:
            if self.loop_depth == 0:
                print(f"ERROR: 'break' used outside of a loop at line {node.line}")

    def visit_ContinueStatement(self, node):
        if not self.in_loop:
            if self.loop_depth == 0:
                print(f"ERROR: 'continue' used outside of a loop at line {node.line}")

    def visit_PrintStatement(self, node):
        for arg in node.printargs:
            self.visit(arg)

    def visit_BinaryExpression(self, node):
                                         
        type1 = self.visit(node.leftexpr)     
        type2 = self.visit(node.rightexpr)    
        op = node.operator
        if type1 is not type2: print(f"ERROR: types in BinExpr differ: {type1} and {type2}.")
        if op not in self.operations: print(f"ERROR: {op} is not an accepable expression.")
        if op in ['!=', '==', '>', '<', '>=', '<=']: return "bool"
        if op in ['+', '-', '*', '/'] and type1 in ['int', 'float', 'str']: return type1
        if op in ['.+', '.-', '*', '/', '.*', './'] and type1 == 'matrix': return type1
        return None
 

    def visit_UnaryExpression(self, node):
        if node.operator in ['UMINUS', 'TRANSPOSE']: return self.visit(node.expr)
        else: raise ValueError(f"Unsupported unary operator: {node.operator}")

    def visit_IdTab(self, node):
        if node.id != 'id': raise ValueError(f"Unsupported id: {node.id}")
        else: 
            self.visit(node.firstexpr)
            self.visit(node.secondexpr)

    def visit_IntNum(self, node):
        return 'int'

    def visit_IDNum(self, node): 
        '''
        czy zmienna juz zadeklarowana w scope
        '''
        symbol = self.current_scope.get(node.id)
        if symbol is None:
            raise NameError(f"Line {node.lineno}: Variable {node.id} has not been declared in this scope.")
        return 'id'

    def visit_StringNum(self, node):
        return 'str'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Matrix(self, node):
        rows = node.matrix

        first_row_length = len(rows[0])
        first_row_type = self.visit(rows[0][0])
        
        for row in rows:
            if len(row) != first_row_length:
                print(f"ERROR: Matrix rows have inconsistent length at line {node.lineno}")
        
            for elem in row:
                t = self.visit(elem)
                if t != first_row_type:
                    print(f"ERROR: Matrix has mixed element types: {first_row_type} and {t} at line {node.lineno}")

        return f"matrix<{first_row_type}>"


    def visit_MatFun(self, node):
        size_type = self.visit(node.intnum)

        if size_type != "int":
            print(f"ERROR: matrix function requires integer size at line {node.lineno}, "f"but got '{size_type}'.")

        return "matrix<float>"

    def visit_IfStatement(self, node):
        '''
        warunek boolem
        '''
        cond = self.visit(node.expr)
        if cond != 'bool':
            raise TypeError(f"Line {node.lineno}: Condition type in if statement is {cond} - has to be bool.")

    def visit_ReturnStatement(self,node):
        return self.visit(node.expr)

    def visit_WhileLoop(self, node):
        '''
        warunek boolem
        '''
        cond = self.visit(node.expr)
        if cond != 'bool':
            raise TypeError(f"Line {node.lineno}: Condition type in if statement is {cond} - has to be bool.")

    def visit_ForLoop(self, node):
        from_type = self.visit(node.fr)
        to_type = self.visit(node.to)

        if from_type != "int":
            print(f"ERROR: for-loop range start should be int, got {from_type} at line {node.lineno}.")
        if to_type != "int":
            print(f"ERROR: for-loop range end should be int, got {to_type} at line {node.lineno}.")

        self.symbolTable.pushScope("for")

        self.symbolTable.put(node.var, VariableSymbol(node.var, "int"))

        self.visit(node.instruction)

        self.symbolTable.popScope()

    def visit_Assignment(self, node):
        '''
        wszystie operatory oprocz "=" musza miec wczesniej zadeklarowana zmienna;
        typy po obu stronach te same
        '''
        op = node.operator
        var = node.value
        expr_type = self.visit(node.expr)
        if op != "=":
            symbol = self.current_scope.get(var)
            if symbol is None:
                raise NameError(f"Line {node.lineno}: Variable {node.id} has not been declared in this scope.")
            
        

        
        
        

    def visit_Block(self, node):
        self.visit(node.instructions)

    def visit_Error(self, node):
        pass