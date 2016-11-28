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
        self.table = SymbolTable(None, "root")
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
            if self.table.get(node.id_) is not None:
                print("Error: Variable '{}' already declared: line {}".\
                    format(node.id_, node.lineno))
            else:
                item = self.table.getGlobal(node.id_)
                #print(item.__class__.__name__ )
                if isinstance(item, SymbolTable.insideTable):
                    print("Error: Function identifier '{}' used as a variable: line {}".format(node.name, node.lineno))
                else:
                    self.table.put(node.id_, VariableSymbol(node.id_, self.actualType))

    def visit_Const(self, node):
        pass
        #self.visit(node.value)

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node.name)
        if isinstance(definition, SymbolTable.insideTable):
            print("Error: Function identifier '{}' used as a variable: line {}".format(node.name, node.line))
        elif definition is None:
            print("Error: Usage of undeclared variable '{0}': line {1}".format(node.name, node.line))
        else:
            return definition.type_

    def visit_String(self, node):
        return 'string'

    def visit_Float(self, node):
        return 'float'

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
                print("Error: Improper returned type, expected {}, got {}: line {}".format(self.actualFun.type, expType, node.lineNo))

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
                                                                                                         node.type_, node.compound_instr.endLine))

    def lookingForReturn(self, node):  # node to jest ccia�o funkcji wy�ej
        if isinstance(node, AST.Instructions):
            nodeList = node.instructions
        elif isinstance(node, list):
            nodeList = node
        elif hasattr(node, "children"):
            return self.lookingForReturn(node.children)
        else:
            nodeList = [node]
        for element in nodeList:
            if element.__class__.__name__ == "ReturnInstruction":
                return True
            elif element.__class__.__name__ == "ChoiceInstruction":
                if (element.alternate_instruction is not None and self.lookingForReturn(element.instruction) and self.lookingForReturn(element.alternate_instruction)):
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
            print("Error: Variable '{}' already declared: line {}".format(node.id_, node.lineno))
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
            print("Error: Illegal operation, {} {} {}: line {}".format(type1, op, type2, node.lineno))
        return ttype[op][type1][type2]

    def visit_Declarations(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

    def visit_Print(self, node):
        self.visit(node.expr_list)

    def visit_ExpressionList(self, node):
        for exp in node.expressions:
            self.visit(exp)

    def visit_FunctionExpression(self, node):
        connectedFunDef = self.table.getGlobal(node.id_)
        if connectedFunDef is None or not isinstance(connectedFunDef, SymbolTable.insideTable):
            print("Error: Call of undefined function '{}': line {}".format(node.id_, node.lineno))
        else:
            if (node.expr_list.lenght()) != len(connectedFunDef.params):
                print("Error: Improper number of args in {} call: line {}".format(node.id_, node.lineno))
            else:
                types =[]
                for x in node.expr_list.expressions:
                    types.append(self.visit(x))
                expectedTypes = connectedFunDef.params
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected and not (actual == "int" and expected == "float"):
                        print("Error: Improper type of args in {} call: line {}".\
                            format(node.id_, node.lineno))
                        break
            return connectedFunDef.type

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        if node.alternate_instruction is not None:
            self.visit(node.alternate_instruction)

    def visit_WhileInstruction(self, node):
        self.inLoop = True
        self.visit(node.condition)
        self.visit(node.instruction)
        self.inLoop = False

    def visit_Assignment(self, node):
        definition = self.table.getGlobal(node.id_)
        type = self.visit(node.expression)
        if definition is None:
            print("Error: Variable '{0}' undefined in current scope: line {1}".format(node.id_, node.lineno))
        elif type != definition.type_:
            if definition.type_ == "float" and definition == "int":
                print("Warning: Possible loss of precision in {0}: line {1].".format(node.id_, node.lineno))
            else:
                if type is not None:
                    print("Error: Assignment of {0} to {1}: line {2}.".format(type, definition.type_, node.line))
