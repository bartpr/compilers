#!/usr/bin/python
class Symbol():
    pass

class VariableSymbol(Symbol):


    def __init__(self, name, type):
        self.id_ = name
        self.type_ = type
    #


class SymbolTable(object):
    def __init__(self, parent, name):
        self.entries = {}
        self.parent = parent
        self.name = name

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        if name not in self.entries.keys():
            self.entries[name] = symbol
        else:
            i = 1
            while True:
                name = "@" * i
                if name not in self.entries.keys():
                    self.entries[name] = symbol
                    break
                else:
                    i += 1

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            ret = self.entries[name]
            return ret
        except:
            return None

    def getParentScope(self):
        return self.parent

    def getGlobal(self, name):
        if self.get(name) is None:
            if self.getParentScope() is not None:
                return self.getParentScope().getGlobal(name)
            else:
                return None
        else:
            return self.get(name)

    class insideTable(Symbol):
        def __init__(self, name, type, table):
            self.name = name
            self.type = type
            self.params = []
            self.table = table

        def loadParamsTypes(self):
            self.params = [x.type_ for x in self.table.entries.values()]

