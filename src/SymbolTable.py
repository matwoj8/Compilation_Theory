#!/usr/bin/python

class Symbol(object):
    def __init__(self, name, type=None,):
        self.name = name
        self.type = type

    def getType(self):
        return self.type


class VariableSymbol(Symbol):

    def __init__(self, name, type, size=None):
        super().__init__(name, type)
        self.size = size


class FunctionSymbol(Symbol):
    def __init__(self, name, return_type, param_types):
        super().__init__(name, return_type)
        self.param_types = param_types


class SymbolTable(object):
    def __repr__(self):
        return f"<Scope {self.name}, symbols={list(self.symbols.keys())}>"


    def __init__(self, name, parent=None): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        
        elif self.parent is not None:
            return self.parent.get(name)
        
        else:
            return None
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        return SymbolTable(name, self)

    def popScope(self):
        pass
    #


