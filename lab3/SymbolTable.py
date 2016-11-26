#!/usr/bin/python
class Symbol():
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, type):

        pass
    #


class SymbolTable(object):
    entries = {}

    def __init__(self, parent, name): # parent scope and symbol table name
        pass
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        pass
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            ret = self.entries[name]
            return ret
        except:
            return None
    #

    def getParentScope(self):
        pass
    #

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #


    class insideTable(Symbol):
        def __init__(self, name, type, table):
            self.name = name
            self.type = type
            self.params = []
            self.table = table

        def loadParamsTypes(self):
            self.params = [x.type for x in self.table.entries.values()]

