#!/usr/bin/python


# class VariableSymbol(Symbol):

#     def __init__(self, name, type):
#         pass
#     #


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}
        if parent is None:
            self.scopes = []
        else:
            self.scopes = parent

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        
        else:
            return None
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        self.scopes.append(name)

    def popScope(self):
        return self.scopes.pop()
    #


