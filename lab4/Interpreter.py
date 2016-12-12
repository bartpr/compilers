
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack()
        self.functionMemory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return eval("a" + node.op + "b", {"a": r1, "b": r2})

        #TODO: ponizszy kutowy komentarz
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        expression_accept = node.expression.accept(self)
        if self.functionMemory.get(node.id_) is not None:
            self.functionMemory.set(node.id_, expression_accept)
        else:
            self.globalMemory.set(node.id_, expression_accept)
        return expression_accept

    # @when(AST.Const)
    # def visit(self, node):
    #     return node.value

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        if self.functionMemory.get(node.name) is not None:
            return self.functionMemory.get(node.name)
        else:
            return self.globalMemory.get(node.name)

    # simplistic while loop interpretation
    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.Program)
    def visit(self, node):
        node.elements.accept(self)

    @when(AST.Elements)
    def visit(self, node):
        for element in node.elements:
            element.accept(self)

    @when(AST.Declarations)
    def visit(self, node):
        for declaration in node.declarations:
            declaration.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self, node.type_)

    @when(AST.Inits)
    def visit(self, node, type_):
        for init in node.inits:
            init.accept(self, type_)

    @when(AST.Init)
    def visit(self, node, type_):
        expression_accept = node.expression.accept(self)
        #TODO: rest

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Print)
    def visit(self, node):
        print(node.expr_list.accept(self)) # to check if end="\n\r" is needed

    @when(AST.LabeledInstruction)
    def visit(self, node):
        node.instruction.accept(self, node.id_)

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        elif node.alternate_instruction is not None
            return node.alternate_instruction.accept(self)

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
                if node.contition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                if node.condition.accept(self):
                    break

    @when(AST.ReturnInstruction)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.CompoundInstruction)
    def visit(self, node):
        #TODO: something with memory
        if node.declarations is not None:
            node.declarations.accept(self)
        if node.instructions_opt is not None;
            node.instructions_opt.accept(self)

    @when(AST.FunctionExpression)
    def visit(self, node):
        #TODO: body

    @when(AST.ExpressionList)
    def visit(self, node):
        for expression in node.expressions:
            expression.accept(self)

    @when(AST.FunctionDefinition)
    def visit(self, node):
        #TODO: body

    @when(AST.ArgumentsList)
    def visit(self, node):
        for arg in node.args:
            arg.accept(self)

    @when(AST.Argument)
    def visit(self, node):
        return node.id_
