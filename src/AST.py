

class Node(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def indentation(self, i):
        print(i * "|\t", end="")

    def accept(self, visitor):
        return visitor.visit(self)


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
      
