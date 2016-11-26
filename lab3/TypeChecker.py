#!/usr/bin/python
import AST
from SymbolTable import *
from collections import defaultdict



ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'
    ttype[op]['string']['string'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['%', '<<', '>>', '|', '&', '^']:
    ttype[op]['int']['int'] = 'int'


class NodeVisitor(object):

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
        self.table = table = SymbolTable(None, "root")
        self.actualType = ""
        self.inLoop = False;





    def visit_Program(self, node):
        self.visit(node.elements)

    def visit_Elements(self, node):
        for element in node.elements:
            self.visit(element)


    def visit_Declaration(self, node):
        self.actualType = node.type_
        self.visit(node.inits)
        self.actualType = ""



    def visit_Inits(self, node):
        for init in node.inits:
            self.visit(init)

    def visit_Init(self, node):
        expType = self.visit(node.expression)
        if not(expType == self.actualType or (expType == "int" and self.actualType  == "float") or (expType == "float" and self.actualType == "int")):
            print("Error: Assignment of {} to {}: line {}".format(expType, self.actualType, node.lineno))
        else:
            if self.table.get(node.name) is not None:
                print("Error: Variable '{}' already declared: line {}".\
                    format(node.name, node.line))
            else:
                item = self.table.getGlobal(node.name)
                if item is not None and item.__class__.__name__ == 'FunctionSymbol':
                    print("Error: Function identifier '{}' used as a variable: line {}".format(node.name, node.lineno))
                else:
                    self.table.put(node.name, VariableSymbol(node.name, self.actualType))

    def visit_Const(self, node):
        self.visit(node.value)

    #TODO check str and const

    def visit_str(selfself, node):
        pass


    def visit_Integer(self, node):
        return 'int'

    def visit_BreakInstruction(self, node):
        if not self.inLoop:
            print("Error: break instruction outside a loop: line {}".format(node.lineNo))

    def visit_ContinueInstruction(self, node):
        if not self.inLoop:
            print("Error: continue instruction outside a loop: line {}".format(node.lineNo))

    def visit_ReturnInstruction(self, node):
        if self.actualFun is None:
            print("Error: return instruction outside a function: line {}".format(node.lineNo))
        else:
            expType = self.visit(node.expression)
            if expType != self.actualFun.type and (self.actualFun.type != "float" or expType != "int") and expType is not None:
                print("Error: Improper returned type, expected {}, got {}: line {}".format(self.actualFun.type, type, node.lineNo))

    def visit_FunctionDefinition(self, node):
        if self.table.get(node.id_):
            print("Error: Redefinition of function '{}': line {}".format(node.id_, node.lineno))
        else:
            newTable = SymbolTable.insideTable(node.id_, node.type_, SymbolTable(self.table, node.id_))
            self.table.put(node.id_, newTable)
            self.actualFun = newTable  # to samo dla whilow itd
            self.table = self.actualFun.table
            if node.args_list is not None:
                self.visit(node.args_list)
            self.visit(node.compound_instr)
            self.table = self.table.getParentScope()
            self.actualFun = None
            if not self.lookingForReturn(node.compound_instr):
                print("Error: Missing return statement in function '{0}' returning {1}: line {2}".format(node.id_,
                                                                                                         node.type_, node.lineno))

    def lookingForReturn(self, node):  # node to jest ccia�o funkcji wy�ej
        if isinstance(node, list):
            nodeList = node
        elif hasattr(node, "children"):
            return self.lookingForReturn(node.children)
        else:
            nodeList = [node]
        for element in nodeList:
            if element.__class__.__name__ == "ReturnInstruction":
                return True
            elif element.__class__.__name__ == "ChoiceInstruction":
                if (element.alternateAction is not None and self.findReturn(
                        element.action) and self.findReturn(element.alternateAction)):
                    return True
            elif element.__class__.__name__ == "CompoundInstruction":
                if (self.lookingForReturn(element.instructions_opt)):
                    return True
        return False


    def visit_ArgumentsList(self, node):
        for arg in node.args:
            self.visit(arg)
        self.actualFun.loadParamsTypes()


    def visit_Argument(self, node):
        if self.table.get(node.id_) is not None:
            print("Error: Variable '{}' already declared: line {}".format(node.name, node.line))
        self.table.put(node.id_, VariableSymbol(node.id_, node.type_))


    def visit_CompoundInstruction(self, node):
        if node.declarations is not None:
            self.visit(node.declarations)
        self.visit(node.instructions_opt)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op
        if ttype[op][type1][type2] is None and (type1 is not None and type2 is not None):
            print("Error: Illegal operation, {} {} {}: line {}".format(type1, op, type2, node.line))
        return ttype[op][type1][type2]

    def visit_Declarations(self, node):
        for declaration in node.declarations:
            self.visit(declaration)