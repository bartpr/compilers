
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
        self.functionMemory = FunctionMemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if type(r1) is int or type(r2) is int:
            return int(eval("a" + node.op + "b", {"a": r1, "b": r2}))
        else:
            return eval("a" + node.op + "b", {"a": r1, "b": r2})

        #TODO: ponizszy kutowy komentarz
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        expression_accept = node.expression.accept(self)
        if self.functionMemory.in_fun() and self.functionMemory.peek().get(node.id_) is not None:
            self.functionMemory.peek().set(node.id_, expression_accept)
        else:
            self.globalMemory.set(node.id_, expression_accept)
        return expression_accept

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        if node.toInt:
            return int(float(node.value))
        else:
            return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        if self.functionMemory.in_fun() and self.functionMemory.peek().get(node.name) is not None:
            return self.functionMemory.peek().get(node.name)
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
        # pass

    @when(AST.Program)
    def visit(self, node):
        node.elements.accept(self)

    @when(AST.Elements)
    def visit(self, node):
        result = []
        for element in node.elements:
            result.append(element.accept(self))
        return result

    @when(AST.Declarations)
    def visit(self, node):
        result = []
        for declaration in node.declarations:
            result.append(declaration.accept(self))
        return result

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self, node.type_)

    @when(AST.Inits)
    def visit(self, node, type_):
        result = []
        for init in node.inits:
            result.append(init.accept(self, type_))
        return result

    @when(AST.Init)
    def visit(self, node, type_):
        if type_ == "int" and type(node.expression) is AST.Float:
            node.expression.toInt = True
        expression_accept = node.expression.accept(self)
        if self.functionMemory.in_fun():
            self.functionMemory.peek().peek().put(node.id_, expression_accept)
        else:
            self.globalMemory.peek().put(node.id_, expression_accept)
        return expression_accept

    @when(AST.Instructions)
    def visit(self, node):
        result = []
        for instruction in node.instructions:
            result.append(instruction.accept(self))
        return result

    @when(AST.Print)
    def visit(self, node):
        for item in node.expr_list.accept(self):
            print(item, end='\r\n')

    @when(AST.LabeledInstruction)
    def visit(self, node):
        pass

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        elif node.alternate_instruction is not None:
            return node.alternate_instruction.accept(self)

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
                if node.condition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                if node.condition.accept(self):
                    break
        pass

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
        if self.functionMemory.in_fun():
            self.functionMemory.peek().push(Memory(node))
        else:
            self.globalMemory.push(Memory(node))
        if node.declarations is not None:
            node.declarations.accept(self)
        if node.instructions_opt is not None:
            node.instructions_opt.accept(self)
        if self.functionMemory.in_fun():
            self.functionMemory.peek().pop()
        else:
            self.globalMemory.pop()

    @when(AST.FunctionExpression)
    def visit(self, node):
        curr_fun = self.globalMemory.get(node.id_)
        curr_fun_mem = Memory(node.id_)
        if node.expr_list is not None:
            for expr_arg, arg in zip(node.expr_list.expressions, curr_fun.args_list.args):
                curr_fun_mem.put(arg.accept(self), expr_arg.accept(self))
        self.functionMemory.push(MemoryStack(curr_fun_mem))
        try:
            curr_fun.compound_instr.accept(self)
        except ReturnValueException as return_value:
            return return_value.value
        finally:
            self.functionMemory.pop()


    @when(AST.ExpressionList)
    def visit(self, node):
        result = []
        for expression in node.expressions:
            result.append(expression.accept(self))
        return result

    @when(AST.FunctionDefinition)
    def visit(self, node):
        self.globalMemory.peek().put(node.id_, node)

    @when(AST.ArgumentsList)
    def visit(self, node):
        result = []
        for arg in node.args:
            result.append(arg.accept(self))
        return result

    @when(AST.Argument)
    def visit(self, node):
        return node.id_
