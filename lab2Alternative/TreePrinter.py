import AST

indentSign = "| "

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return indentSign * indent + str(self.value) + "\n"

    @addToClass(AST.ExpressionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.expressionList))

    @addToClass(AST.ArgumentList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.argList))

    @addToClass(AST.Argument)
    def printTree(self, indent=0):
        return indentSign * indent + "ARG " + self.name + "\n"

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return indentSign * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)

    @addToClass(AST.GroupedExpression)
    def printTree(self, indent=0):
        return self.interior.printTree(indent)

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent=0):
        return ("" if self.declarations is None else self.declarations.printTree(indent + 1)) + \
            self.instructions.printTree(indent + 1)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "LABEL\n" + indentSign * (indent + 1) + str(self.id) + "\n" + \
               self.instr.printTree(indent + 1)

    @addToClass(AST.InvocationExpression)
    def printTree(self, indent=0):
        return indentSign * indent + "FUNCALL\n" + indentSign * (indent + 1) + str(self.name) + "\n" + \
               self.args.printTree(indent+1)

    @addToClass(AST.FunctionExpressionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.fundefs))



    @addToClass(AST.DeclarationList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.declarations))

    @addToClass(AST.ComponentList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.components))

    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        return indentSign * indent + "DECL\n" + self.inits.printTree(indent + 1)

    @addToClass(AST.InitList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.inits))

    @addToClass(AST.Init)
    def printTree(self, indent=0):
        return indentSign * indent + "=\n" + indentSign * (indent + 1) + str(self.name) + "\n" + \
               self.expr.printTree(indent + 1)

    @addToClass(AST.InstructionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.instructions))

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "PRINT\n" + self.expr.printTree(indent + 1)

    @addToClass(AST.AssignmentInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "=\n" + indentSign * (indent + 1) + str(self.id) + "\n" + \
               self.expr.printTree(indent + 1)

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "IF\n" + self.condition.printTree(indent + 1) + self.action.printTree(indent + 1) + \
               ("" if self.alternateAction is None else indentSign * indent + "ELSE\n" +
                                                        self.alternateAction.printTree(indent + 1))

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "WHILE\n" + self.condition.printTree(indent + 1) + self.instruction.printTree(indent)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "REPEAT\n" + self.instructions.printTree(indent + 1) + indentSign * indent + \
            "UNTIL\n" + self.condition.printTree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "RETURN\n" + self.expression.printTree(indent + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        return indentSign * indent + "CONTINUE\n"

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        return self.components.printTree()


