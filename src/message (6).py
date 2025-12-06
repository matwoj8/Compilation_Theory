import lab3.AST as AST
from lab4.SymbolTable import SymbolTable


class NodeVisitor(object):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.current_scope = self.symbol_table
        self.loop_indent = 0

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            for item in child:
                if isinstance(item, AST.Node):
                    self.visit(item)

            if isinstance(child, AST.Node):
                self.visit(child)


class TypeCheckerHelper:
    def __init__(self):
        self.operations = {}

    def add_operation(self, op, type1, type2, result_type):
        self.operations[op] = self.operations.get(op, {})
        self.operations[op][type1] = self.operations[op].get(type1, {})
        self.operations[op][type1][type2] = result_type

    def check_types(self, op, type1, type2, lineno):
        if op in self.operations and type1 in self.operations[op] and type2 in self.operations[op][type1]:
            return self.operations[op][type1][type2]
        else:
            print(f"Line nr:{lineno} - Type error: {type1} {op} {type2} is not correct")
            return None


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.type_checker_helper = TypeCheckerHelper()

        operations = [
            ["+", "int", "int", "int"],
            ["+", "int", "float", "float"],
            ["+", "float", "int", "float"],
            ["+", "float", "float", "float"],
            ["+", "str", "str", "str"],
            ["+", "vector", "vector", "vector"],

            ["-", "int", "int", "int"],
            ["-", "int", "float", "float"],
            ["-", "float", "int", "float"],
            ["-", "float", "float", "float"],
            ["-", "vector", "vector", "vector"],

            ["*", "int", "int", "int"],
            ["*", "int", "float", "float"],
            ["*", "float", "int", "float"],
            ["*", "float", "float", "float"],
            ["*", "vector", "vector", "vector"],
            ["*", "str", "int", "str"],
            ["*", "int", "str", "str"],

            ["/", "int", "int", "int"],
            ["/", "int", "float", "float"],
            ["/", "float", "int", "float"],
            ["/", "float", "float", "float"],
            ["/", "vector", "vector", "vector"],

            [">", "int", "int", "bool"],
            [">", "int", "float", "bool"],
            [">", "float", "int", "bool"],
            [">", "float", "float", "bool"],
            [">", "vector", "vector", "bool"],

            ["<", "int", "int", "bool"],
            ["<", "int", "float", "bool"],
            ["<", "float", "int", "bool"],
            ["<", "float", "float", "bool"],
            ["<", "vector", "vector", "bool"],

            [">=", "int", "int", "bool"],
            [">=", "int", "float", "bool"],
            [">=", "float", "int", "bool"],
            [">=", "float", "float", "bool"],
            [">=", "vector", "vector", "bool"],

            ["<=", "int", "int", "bool"],
            ["<=", "int", "float", "bool"],
            ["<=", "float", "int", "bool"],
            ["<=", "float", "float", "bool"],
            ["<=", "vector", "vector", "bool"],

            ["==", "int", "int", "bool"],
            ["==", "int", "float", "bool"],
            ["==", "float", "int", "bool"],
            ["==", "float", "float", "bool"],
            ["==", "str", "str", "bool"],
            ["==", "vector", "vector", "bool"],

            ["!=", "int", "int", "bool"],
            ["!=", "int", "float", "bool"],
            ["!=", "float", "int", "bool"],
            ["!=", "float", "float", "bool"],
            ["!=", "str", "str", "bool"],
            ["!=", "vector", "vector", "bool"],

            [".+", "vector", "vector", "vector"],
            [".-", "vector", "vector", "vector"],
            [".*", "vector", "vector", "vector"],
            ["./", "vector", "vector", "vector"]
        ]

        for op, type1, type2, result_type in operations:
            self.type_checker_helper.add_operation(op, type1, type2, result_type)

    def visit_InstructionsOrEmpty(self, node: AST.InstructionsOrEmpty):
        self.visit(node.instructions)

    def visit_Instructions(self, node: AST.Instructions):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Id(self, node: AST.Id):
        return self.symbol_table.get(node.id)

    def visit_BinaryExpression(self, node: AST.BinaryExpression):
        node.v_type = 'float'
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        result_type = self.type_checker_helper.check_types(op, type1, type2, node.lineno)

        if result_type is None:
            print(f"Line nr:{node.lineno} - Type error: {type1} {op} {type2} is not correct")
            return None

        if type1 == "vector" or type2 == "vector":
            if isinstance(node.left, AST.Id):
                left_dims = self.symbol_table.get_v_dims(node.left.id)
                node.v_type = self.symbol_table.get_v_type(node.left.id)
            elif isinstance(node.left, AST.BinaryExpression):
                left_dims = node.left.dims
            elif isinstance(node.left, AST.Vector):
                left_dims = node.left.dims
            else:
                print(f"Error in visit_BinaryExpression {node.left} {type1} {type2}")
                return
            if isinstance(node.right, AST.Id):
                right_dims = self.symbol_table.get_v_dims(node.right.id)
                node.v_type = self.symbol_table.get_v_type(node.left.id)
            elif isinstance(node.right, AST.BinaryExpression):
                right_dims = node.right.dims
            elif isinstance(node.right, AST.Vector):
                right_dims = node.right.dims
            else:
                print("Error in visit_BinaryExpression")
                return

            if len(right_dims) != len(left_dims):
                print(f"Line nr:{node.lineno} - Nonequal vector dimentions -", len(right_dims), len(left_dims))
                return None

            for i in range(len(right_dims)):
                if left_dims[i] != right_dims[i]:
                    if hasattr(left_dims[0], 'intnum') and left_dims[0].intnum != right_dims[0].intnum:
                        print(f"Line nr:{node.lineno} - Nonequal vector dim -", left_dims[0].intnum,
                              right_dims[0].intnum)
                    return None
            node.dims = left_dims
        return result_type

    def visit_IfStatement(self, node: AST.IfStatement):
        self.symbol_table = self.symbol_table.pushScope("if")

        self.visit(node.cond)
        self.visit(node.if_body)
        self.symbol_table = self.symbol_table.popScope()
        if node.else_body is not None:
            self.symbol_table = self.symbol_table.pushScope("else")
            self.visit(node.else_body)
            self.symbol_table = self.symbol_table.popScope()

    def visit_ReturnStatement(self, node: AST.ReturnStatement):
        return self.visit(node.expr)

    def visit_BreakStatement(self, node: AST.BreakStatement):
        if self.loop_indent == 0:
            print(f"Line nr:{node.lineno} - Break shouldn't be here")

    def visit_ContinueStatement(self, node: AST.ContinueStatement):
        if self.loop_indent == 0:
            print(f"Line nr:{node.lineno} - Continue shouldn't be here")

    def visit_ForLoop(self, node: AST.ForLoop):
        self.symbol_table = self.symbol_table.pushScope('for')
        self.loop_indent += 1
        t1 = self.visit(node.cond_start)
        t2 = self.visit(node.cond_end)

        if t1 is None or t2 is None or t1 != t2:
            print(f"Line nr:{node.lineno} - something wrong with operand types")
            self.symbol_table.put(node.id, None)

        else:
            if isinstance(node.id, AST.Id):
                self.symbol_table.put(node.id.id, t1)
            else:
                self.symbol_table.put(node.id, t1)

        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1

    def visit_WhileLoop(self, node: AST.WhileLoop):
        self.symbol_table = self.symbol_table.pushScope("while")
        self.loop_indent += 1
        self.visit(node.cond)
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1

    def visit_Assignment(self, node: AST.Assignment):
        val_type = self.visit(node.right)
        if val_type is None:
            return None
        left_id = node.left.id
        if node.op == '=':

            if isinstance(left_id, str):
                self.symbol_table.put(left_id, val_type)
            else:
                self.symbol_table.put(left_id.id, val_type)

            if val_type == 'vector':
                if isinstance(node.right.dims, AST.IntNum):
                    self.symbol_table.v_dims[left_id] = node.right.dims.intnum
                    self.symbol_table.v_type[left_id] = node.right.v_type
                else:
                    self.symbol_table.v_dims[left_id] = node.right.dims
                    self.symbol_table.v_type[left_id] = node.right.v_type
        else:
            var_type = self.symbol_table.get(left_id)
            if var_type == 'vector' and val_type == 'vector':
                var_d = self.symbol_table.v_dims[left_id]
                val_d = node.right.dims

                if len(var_d) != len(val_d):
                    print(f"Line nr:{node.lineno} - wrong dimensions")
                    return None

                for i in range(len(var_d)):
                    if var_d[i] != val_d[i]:
                        print(f"Line nr:{node.lineno} - wrong dimensions")
                        return None

            result_type = self.type_checker_helper.check_types(node.op[0], var_type, val_type, node.lineno)
            if result_type is None:
                print(f"Line nr:{node.lineno} - operation on given values is not defined")
            return result_type

    def visit_Vector(self, node: AST.Vector):
        if isinstance(node.vector[0], AST.Vector):
            d = node.vector[0].dims
        else:
            d = [1]

        for e in node.vector:
            if isinstance(e, AST.Vector):
                self.visit(e)
                ed = e.dims
            else:
                ed = [1]

            for i in range(len(d)):
                if d[i] != ed[i]:
                    print(f"Line nr:{node.lineno} - Wrong vector size")
                    return None
        return 'vector'

    def visit_PrintStatement(self, node: AST.PrintStatement):
        for i in node.printargs:
            self.visit(i)

    def visit_StringLiteral(self, node: AST.StringLiteral):
        return 'str'

    def visit_IntNum(self, node: AST.IntNum):
        return 'int'

    def visit_Float(self, node: AST.Float):
        return 'float'

    def visit_Variable(self, node: AST.Variable):
        if not node.id.id in self.symbol_table.v_dims: return
        dims = self.symbol_table.v_dims[node.id.id]

        if len(dims) != len(node.index):
            print(f"Line nr:{node.lineno} - Trying to access non-existing dimension")
            return None

        for i in range(len(node.index)):
            if self.visit(node.index[i]) != 'int':
                print(f"Line nr:{node.lineno} - Vector index must be int")
                return None

            if callable(hasattr(node.index[i], 'intnum')) and node.index[i].intnum >= dims[i].intnum:
                print(f"Line nr:{node.lineno} - Index out of ouns")
                return None

        return self.symbol_table.v_type[node.id.id]

    def visit_UnaryExpression(self, node: AST.UnaryExpression):
        return self.visit(node.expr)

    def visit_MatFun(self, node: AST.MatFun):
        for el in node.dims:
            if self.visit(el) != 'int':
                print(f"Line nr:{node.lineno} - matrix function takes int")
                return None
        return 'vector'

