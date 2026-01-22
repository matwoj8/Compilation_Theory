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
    
    def _is_vector(self, size):
        """Sprawdza czy rozmiar odpowiada wektorowi (jedna z wymiarów = 1)."""
        if size is None:
            return False
        rows, cols = size
        return rows == 1 or cols == 1

    def _check_matrix_indices(self, idtab_node, symbol, lineno):
        """
        Sprawdza czy indeksy mieszczą się w zakresie macierzy/wektora.
        """
        print(f"DEBUG _check_matrix_indices:")
        print(f"  id = {idtab_node.id}")
        print(f"  symbol.type = {symbol.type}")
        print(f"  symbol.size = {symbol.size}")
        print(f"  firstexpr = {idtab_node.firstexpr}")
        print(f"  secondexpr = {idtab_node.secondexpr}")
        if not self._is_matrix_type(symbol.type):
            raise TypeError(f"Line {lineno}: Variable {idtab_node.id} is not a matrix or vector.")
        
        if symbol.size is None:
            return
        print(f"  size = {symbol.size}")
        rows, cols = symbol.size
        
        # Sprawdź czy to wektor
        is_vector = rows == 1 or cols == 1
        
        # Dla wektora używamy tylko jednego indeksu
        if is_vector and idtab_node.secondexpr:
            raise TypeError(f"Line {lineno}: Vector indexing requires only one index.")
        
        # Sprawdź pierwszy indeks
        if isinstance(idtab_node.firstexpr, AST.IntNum):
            idx1 = idtab_node.firstexpr.intnum
            
            if is_vector:
                # Dla wektora - indeksujemy elementy
                total_elements = max(rows, cols)  # dla wektora rows lub cols = 1
                if idx1 < 1 or idx1 > total_elements:
                    raise IndexError(f"Line {lineno}: Vector index {idx1} out of range [1, {total_elements}].")
            else:
                # Dla macierzy - pierwszy indeks to wiersz
                if idx1 < 1 or idx1 > rows:
                    raise IndexError(f"Line {lineno}: Row index {idx1} out of range [1, {rows}].")
        
        # Sprawdź drugi indeks (tylko dla macierzy)
        if idtab_node.secondexpr and isinstance(idtab_node.secondexpr, AST.IntNum):
            if is_vector:
                raise TypeError(f"Line {lineno}: Vector indexing requires only one index.")
            
            idx2 = idtab_node.secondexpr.intnum
            if idx2 < 1 or idx2 > cols:
                raise IndexError(f"Line {lineno}: Column index {idx2} out of range [1, {cols}].")

    def visit_InstructionsOrEmpty(self, node):
        if node.instructions is not None:
            return self.visit(node.instructions)
        return None

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

        if op in ['.+', '.-', '.*', './']:
            if self._is_matrix_type(type1) and self._is_matrix_type(type2):
                e1 = self._matrix_elem_type(type1)
                e2 = self._matrix_elem_type(type2)
                if e1 != e2:
                    raise TypeError(f"Line {node.lineno}: Matrix element types differ: {e1} vs {e2}.")

                # Pobierz rozmiar lewego wyrażenia
                left_size = node.leftexpr.size if hasattr(node.leftexpr, 'size') else None
                
                # Pobierz rozmiar prawego wyrażenia
                right_size = node.rightexpr.size if hasattr(node.rightexpr, 'size') else None

                print(f"DEBUG: lineno {node.lineno}, left_size = {left_size}, right_size = {right_size}")
                
                if left_size and right_size and left_size != right_size:
                    raise ValueError(f"Line {node.lineno}: Matrix sizes do not match for operation {op}: {left_size} vs {right_size}.")
                
                # Ustaw rozmiar dla wyniku operacji
                if left_size:
                    node.size = left_size
                elif right_size:
                    node.size = right_size

                else:
                    if isinstance(node.leftexpr, AST.IDNum):
                        symbol = self.current_scope.get(node.leftexpr.id)
                        if symbol and hasattr(symbol, 'size'):
                            node.size = symbol.size
                    elif isinstance(node.rightexpr, AST.IDNum):
                        symbol = self.current_scope.get(node.rightexpr.id)
                        if symbol and hasattr(symbol, 'size'):
                            node.size = symbol.size
                
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
                expr_size = None
                if hasattr(node.expr, 'size'):
                    expr_size = node.expr.size
                elif isinstance(node.expr, AST.IDNum):
                    symbol = self.current_scope.get(node.expr.id)
                    if symbol and symbol.size:
                        expr_size = symbol.size
                
                if expr_size:
                    rows, cols = expr_size
                    node.size = (cols, rows)
                return type_expr
            else:
                raise TypeError(f"Line {node.lineno}: Can't use operator {node.operator} with type {type_expr}.")

        else: raise ValueError(f"Line {node.lineno}: Unsupported unary operator: {node.operator}")

    def visit_IdTab(self, node):
        # Sprawdź typy indeksów
        idx1_type = self.visit(node.firstexpr)
        if idx1_type != 'int':
            raise TypeError(f"Line {node.lineno}: First index must be of type int, got {idx1_type}.")
        
        if node.secondexpr:
            idx2_type = self.visit(node.secondexpr)
            if idx2_type != 'int':
                raise TypeError(f"Line {node.lineno}: Second index must be of type int, got {idx2_type}.")
        
        var_name = node.id
        symbol = self.current_scope.get(var_name)
        if hasattr(node, 'size'):
            node.size = symbol.size
            
        if symbol is None:
            raise NameError(f"Line {node.lineno}: Variable {var_name} has not been declared in this scope.")
        
        if not self._is_matrix_type(symbol.type):
            raise TypeError(f"Line {node.lineno}: Variable {var_name} is not a matrix or vector.")
        
        # Sprawdź zakresy indeksów
        self._check_matrix_indices(node, symbol, node.lineno)
        
        # Zwróć typ elementu
        return self._matrix_elem_type(symbol.type)

    def visit_IntNum(self, node):
        return 'int'

    def visit_IDNum(self, node): 
        '''
        czy zmienna juz zadeklarowana w scope
        '''
        print(f"DEBUG visit_IDNum: Looking for variable '{node.id}' in scope")
        print(f"DEBUG visit_IDNum: Current scope name = {self.current_scope.name}")
        symbol = self.current_scope.get(node.id)
        if symbol is None:
            raise NameError(f"Line {node.lineno}: Variable {node.id} has not been declared in this scope.")
        
        if hasattr(node, 'size'):
            node.size = symbol.size

        return symbol.getType()

    def visit_StringNum(self, node):
        return 'str'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Matrix(self, node):
        rows = node.matrix

        if isinstance(rows, list) and rows and isinstance(rows[0], AST.Matrix):
            rows = [row.matrix for row in rows]

        # sztuczny poziom listy dodany przez parser
        if (
            isinstance(rows, list)
            and len(rows) == 1
            and isinstance(rows[0], list)
        ):
            rows = rows[0]
        node.matrix = rows
        print(f"DEBUG visit_Matrix: rows = {rows}")

        
        # Sprawdź czy to wektor (lista elementów) czy macierz (lista list)
        is_vector = not isinstance(rows[0], AST.Matrix)
        
        if is_vector:
            # Wektor wierszowy: [1, 2, 3]
            first_elem_type = self.visit(rows[0])
            vector_length = len(rows)
            
            for i in range(1, len(rows)):
                elem_type = self.visit(rows[i])
                if elem_type != first_elem_type:
                    raise TypeError(f"Line {node.lineno}: Inconsistent element types in vector: expected {first_elem_type}, got {elem_type}.")
            
            # Wektor wierszowy: 1 wiersz, n kolumn
            node.size = (1, vector_length)
            return f"matrix<{first_elem_type}>"
        
        else:
            # Sprawdź czy to wektor kolumnowy (lista list z jednym elementem w każdym wierszu)
            first_element_is_list = isinstance(rows[0], AST.Matrix)
            print(f"DEBUG: first_element_is_list = {first_element_is_list}")
            print(f"DEBUG: rows  = {rows}")
            print(f"DEBUG: rows[0].matrix = {rows[0].matrix[0] if first_element_is_list else 'N/A'}")
            if first_element_is_list and len(rows[0].matrix[0]) == 1:
                print("DEBUG: Possible column vector detected.")
                # Potencjalny wektor kolumnowy: [[1], [2], [3]]
                # Sprawdź czy wszystkie wiersze mają po jednym elemencie
                is_column_vector = all(len(row) == 1 for row in rows)
                if is_column_vector:
                    # Wektor kolumnowy
                    first_elem_type = self.visit(rows[0][0])
                    vector_length = len(rows)
                    
                    for i in range(1, len(rows)):
                        elem_type = self.visit(rows[i][0])
                        if elem_type != first_elem_type:
                            raise TypeError(f"Line {node.lineno}: Inconsistent element types in column vector: expected {first_elem_type}, got {elem_type}.")
                    
                    node.size = (vector_length, 1)
                    return f"matrix<{first_elem_type}>"
            
            # Macierz dwuwymiarowa
            first_row = rows[0]  # AST.Matrix
            first_row_length = len(first_row.matrix[0])  # Długość pierwszej listy elementów
            first_element = first_row.matrix[0][0]  # Pierwszy element
            first_element_type = self.visit(first_element)  # Typ pierwszego elementu
            matrix_size = (len(rows), first_row_length)

            print(f"DEBUG: Matrix size = {matrix_size}, first_element_type = {first_element_type}")
            print(f"DEBUG: first_row.matrix = {first_row.matrix}")
            
            for i, row_obj in enumerate(rows):
                # row_obj to AST.Matrix, row_obj.matrix to lista elementów
                row_elements = row_obj.matrix[0]
                if len(row_elements) != first_row_length:
                    raise ValueError(f"Line {node.lineno}: Inconsistent row sizes in matrix: row {i+1} has {len(row_elements)} elements, expected {first_row_length}.")
                
                for j, elem in enumerate(row_elements):
                    elem_type = self.visit(elem)
                    if elem_type != first_element_type:
                        raise TypeError(f"Line {node.lineno}: Inconsistent element types in matrix at position [{i+1},{j+1}]: expected {first_element_type}, got {elem_type}.")
            
            node.size = matrix_size
            return f"matrix<{first_element_type}>"


    def visit_MatFun(self, node):
        size_type = self.visit(node.intnum)

        if size_type != "int":
            raise TypeError(f"Line {node.lineno}: Matrix size must be of type int, got {size_type}.")

        node.size = (int(node.intnum.intnum), int(node.intnum.intnum))
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
        

        print(f"DEBUG: Declaring loop variable {node.id.id} of type int in for-loop at line {node.lineno}.")
        
        print(self.current_scope)
        from_type = self.visit(node.firstexpr)
        to_type = self.visit(node.secondexpr)

        self.current_scope = self.current_scope.pushScope(f"for_{node.lineno}")
        self.current_scope.put(node.id.id, VariableSymbol(node.id.id, "int"))

        if from_type != "int":
            raise TypeError(f"ERROR: for-loop range start should be int, got {from_type} at line {node.lineno}.")
        if to_type != "int":
            raise TypeError(f"ERROR: for-loop range end should be int, got {to_type} at line {node.lineno}.")

        

        self.loop_depth += 1
        print(self.current_scope)

        self.visit(node.instruction)

        self.current_scope = self.current_scope.getParentScope()

        self.loop_depth -= 1

    def visit_Assignment(self, node):
        op = node.operator
        expr_type = self.visit(node.expr)  # typ prawej strony

        if isinstance(node.value, AST.IDNum):
            var_name = node.value.id
            if op != "=":
                # dla +=, -=, itd.
                symbol = self.current_scope.get(var_name)
                if symbol is None:
                    raise NameError(f"Line {node.lineno}: Variable {var_name} has not been declared in this scope.")
                var_type = symbol.getType()
            else:
                # dla = - zapisz zmienną z rozmiarem jeśli istnieje
                size = None
                if hasattr(node.expr, 'size'):
                    size = node.expr.size

                self.current_scope.put(
                    var_name,
                    VariableSymbol(var_name, expr_type, size)
                )
        
        elif isinstance(node.value, AST.IdTab):
            # Dla przypisania do elementu macierzy/wektora
            
            # Pobierz nazwę zmiennej i symbol
            var_name = node.value.id
            symbol = self.current_scope.get(var_name)
            
            if symbol is None:
                raise NameError(f"Line {node.lineno}: Variable {var_name} has not been declared in this scope.")
            
            # Sprawdź indeksy i typ elementu
            element_type = self.visit_IdTab(node.value)
            
            # Sprawdź zgodność typów
            if expr_type != element_type:
                # Pozwól na int -> float
                if element_type == 'int' and expr_type == 'float':
                    pass  # OK
                elif element_type == 'float' and expr_type == 'int':
                    pass  # OK
                else:
                    raise TypeError(f"Line {node.lineno}: Cannot assign {expr_type} to element of type {element_type}.")
                
        else:
            raise TypeError(f"Line {node.lineno}: Invalid assignment target.")

    def visit_Block(self, node):
        self.visit(node.instructions)

    def visit_Error(self, node):
        pass