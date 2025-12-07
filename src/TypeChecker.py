from SymbolTable import *
from AST import Node
import AST


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
        self.global_scope = SymbolTable("global")
        self.current_scope = self.global_scope
        self.loop_depth = 0

    def _is_matrix_type(self, t):
        return isinstance(t, str) and t.startswith("matrix<") and t.endswith(">")
    
    def _matrix_elem_type(self, t):
        if self._is_matrix_type(t):
            return t[len("matrix<"):-1]
        return None

    def visit_InstructionOrEmpty(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BreakStatement(self, node):
        if self.loop_depth == 0:
            raise SyntaxError(f"Line {node.lineno}: 'break' used outside of a loop.")

    def visit_ContinueStatement(self, node):
        if self.loop_depth == 0:
            raise SyntaxError(f"Line {node.lineno}: 'continue' used outside of a loop.")

    def visit_PrintStatement(self, node):
        for arg in node.printargs:
            self.visit(arg)

    def visit_BinaryExpression(self, node):
                                         
        type1 = self.visit(node.leftexpr)     
        type2 = self.visit(node.rightexpr)    
        op = node.operator

        if op not in self.operations: print(f"ERROR: {op} is not an acceptable expression.")

        if type1 == 'str' or type2 == 'str':
            if type1 == 'str' and type2 == 'str':
                if op == '+':
                    return 'str'
                else:
                    raise TypeError(f"Line {node.lineno}: Can't use operator {op} with strings.")
            else:
                raise TypeError(f"Line {node.lineno}: Can't mix string with non-string using {op}.")

        if op in ['.+', '.-', '.*', './', '.*', './']:
            if self._is_matrix_type(type1) and self._is_matrix_type(type2):
                e1 = self._matrix_elem_type(type1)
                e2 = self._matrix_elem_type(type2)
                if e1 != e2:
                    raise TypeError(f"Line {node.lineno}: Matrix element types differ: {e1} vs {e2}.")
                return type1  # matrix<elem>
            else:
                raise TypeError(f"Line {node.lineno}: Matrix operator {op} requires both operands to be matrices.")

        if op in ['!=', '==', '>', '<', '>=', '<=']:
            if (type1 in ('int','float') and type2 in ('int','float')) or type1 == type2:
                return 'bool'
            else:
                raise TypeError(f"Line {node.lineno}: Can't compare types {type1} and {type2} with {op}.")

        numeric_ops = ['+', '-', '*', '/']
        if op in numeric_ops:
            if type1 in ('int', 'float') and type2 in ('int','float'):
                if type1 == 'float' or type2 == 'float':
                    return 'float'
                else:
                    return 'int'
            else:
                raise TypeError(f"Line {node.lineno}: Operator {op} requires numeric operands, got {type1} and {type2}.")

        raise TypeError(f"Line {node.lineno}: Unsupported binary operation {op} for types {type1}, {type2}.")


    def visit_UnaryExpression(self, node):
        type_expr = self.visit(node.expr)
        if node.operator == 'UMINUS':
            if type_expr in ['int', 'float'] or self._is_matrix_type(type_expr):
                return type_expr
            else:
                raise TypeError(f"Line {node.lineno}: Can't use operator {node.operator} with type {type_expr}.")

        elif node.operator == 'TRANSPOSE':
            if self._is_matrix_type(type_expr):
                return type_expr
            else:
                raise TypeError(f"Line {node.lineno}: Can't use operator {node.operator} with type {type_expr}.")

        else: raise ValueError(f"Line {node.lineno}: Unsupported unary operator: {node.operator}")

    def visit_IdTab(self, node):
        self.visit(node.firstexpr)
        if node.secondexpr:
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
        return symbol.getType()

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
                print(f"Line {node.lineno}: Matrix rows have inconsistent length.")

            for elem in row:
                t = self.visit(elem)
                if t != first_row_type:
                    print(f"Line {node.lineno}: Matrix has mixed element types: {first_row_type} and {t}.")

        return f"matrix<{first_row_type}>"


    def visit_MatFun(self, node):
        size_type = self.visit(node.intnum)

        if size_type != "int":
            print(f"Line {node.lineno}: matrix function requires integer size, but got '{size_type}'.")

        return "matrix<float>"

    def visit_IfStatement(self, node):
        '''
        warunek boolem
        '''
        cond = self.visit(node.expr)
        if cond != 'bool':
            raise TypeError(f"Line {node.lineno}: Condition type in if statement is {cond} - has to be bool.")
        
        self.current_scope = self.current_scope.pushScope("if")
        self.visit(node.firstinstruction)
        self.current_scope = self.current_scope.getParentScope()
        if node.secondinstruction:
            self.current_scope = self.current_scope.pushScope("else")
            self.visit(node.secondinstruction)
            self.current_scope = self.current_scope.getParentScope()
        

    def visit_ReturnStatement(self,node):
        return self.visit(node.expr)

    def visit_WhileLoop(self, node):
        '''
        warunek boolem
        '''
        cond = self.visit(node.expr)
        if cond != 'bool':
            raise TypeError(f"Line {node.lineno}: Condition type in if statement is {cond} - has to be bool.")

        self.loop_depth += 1
        self.current_scope = self.current_scope.pushScope("while")
        self.visit(node.instruction)
        self.current_scope = self.current_scope.getParentScope()
        self.loop_depth -= 1

    def visit_ForLoop(self, node):
        from_type = self.visit(node.fr)
        to_type = self.visit(node.to)

        if from_type != "int":
            print(f"ERROR: for-loop range start should be int, got {from_type} at line {node.lineno}.")
        if to_type != "int":
            print(f"ERROR: for-loop range end should be int, got {to_type} at line {node.lineno}.")

        self.current_scope = self.current_scope.pushScope("for")

        self.current_scope.put(node.var, VariableSymbol(node.var, "int"))

        self.loop_depth += 1
        self.visit(node.instruction)

        self.current_scope = self.current_scope.getParentScope()

        self.loop_depth -= 1

    def visit_Assignment(self, node):
        '''
        wszystie operatory oprocz "=" musza miec wczesniej zadeklarowana zmienna;
        typy po obu stronach te same
        '''
        op = node.operator
        var_name = node.value
        expr_type = self.visit(node.expr)

        if op != "=":
            symbol = self.current_scope.get(var_name)
            if symbol is None:
                raise NameError(f"Line {node.lineno}: Variable {var_name} has not been declared in this scope.")

            var_type = symbol.getType()
            if op in ['+=', '-=', '*=', '/=']:
                if var_type in ('int','float') and expr_type in ('int','float'):
                    if var_type == 'float' or expr_type == 'float':
                        result_type = 'float'
                    else:
                        result_type = 'int'
                else:
                    raise TypeError(f"Line {node.lineno}: Operator {op} requires numeric operands, got {var_type} and {expr_type}.")
            else:
                raise ValueError(f"Line {node.lineno}: Unsupported assignment operator: {op}")
            
        else:
            self.current_scope.put(var_name, VariableSymbol(var_name, expr_type))

    def visit_Block(self, node):
        self.current_scope = self.current_scope.pushScope("block")
        self.visit(node.instructions)
        self.current_scope = self.current_scope.getParentScope()

    def visit_Error(self, node):
        pass