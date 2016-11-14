import AST

LEVEL_TOKEN = "| "

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, level=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        return  "| " * level + self.op + "\n" + self.left.printTree(level + 1) + self.right.printTree(level + 1)

    @addToClass(AST.Const)
    def printTree(self, level=0):
        ret = level * "| "
        ret = ret + str(self.value)
        return ret

    @addToClass(AST.Integer)
    def printTree(self, level=0):
        ret = "| " * level
        ret = ret + str(self.value)
        return ret

    @addToClass(AST.Float)
    def printTree(self, level=0):
        ret = "| " * level
        ret = ret + str(self.value)
        return ret

    @addToClass(AST.String)
    def printTree(self, level=0):
        ret = "| " * level
        ret = ret + str(self.value)
        return ret

    @addToClass(AST.Program)
    def printTree(self, level=0):
        return self.elements.printTree()

    @addToClass(AST.Declarations)
    def printTree(self):
        ret = ""
        x = ""
        for d in self.declarations:
            ret += x + str(d)
            x = "\n"
        return ret

    @addToClass(AST.Declaration)
    def printTree(self, level = 0):
        ret = "| " * level
        ret = ret + "DECL\n" + self.inits.printTree(level + 1)
        return ret

    @addToClass(AST.Inits)
    def printTree(self, level=0):
        ret = "| " * level
        level += 1
        for i in self.inits:
            ret += "=\n" + str(i) + "\n"
        level -= 1
        return ret

    @addToClass(AST.Init)
    def printTree(self, level = 0):
        ret = "| " * level
        ret = ret + str(self.id_) + "\n" + str(self.expression)
        return ret

    @addToClass(AST.Instructions)
    def printTree(self, level = 0):
        ret = ""
        x = ""
        for i in self.instructions:
            ret += x + str(i)
            x = "\n"
        return ret

    @addToClass(AST.Print)
    def printTree(self, level):
        ret = "| " * level
        #tutaj nie jestem pewien
        ret += "PRINT\n" + str(self.expr_list)
        return ret


    @addToClass(AST.LabeledInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "LABEL\n" + "| " *(1+level) + str(self.id) + "\n" + self.instruction.printTree(level + 1)

    @addToClass(AST.Assignment)
    def printTree(self, level=0):
        return "| " * level + "=\n" + "| "  * (level + 1) + str(self.id_) + "\n" + self.expression.printTree(level + 1)


    @addToClass(AST.WhileInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "WHILE\n" + self.condition.printTree(level + 1) + self.instruction.printTree(level)


    @addToClass(AST.RepeatInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "REPEAT\n" + self.instructions.printTree(level + 1) + "| "  * level + "UNTIL\n" + self.condition.printTree(level + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "RETURN\n" + self.expression.printTree(level + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "CONTINUE\n"

    @addToClass(AST.CompoundInstruction)
    def printTree(self, level=0):
        return ("" if self.declarations is None else self.declarations.printTree(level + 1)) + self.instructions.printTree(level + 1)

    @addToClass(AST.GroupedExpression)
    def printTree(self, level=0):
        #sprawdzic
        return self.expressions.printTree(level)

    @addToClass(AST.FunctionExpression)
    def printTree(self, level=0):
        ret = "| " * level #trzeba uzupelnic
        return ret

    @addToClass(AST.ExpressionList)
    def printTree(self, level=0):
        ret = ""
        for e in self.expression:
            ret += str(e) + "\n"
        return ret



    @addToClass(AST.FunctionExpression)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "FUNDEF\n" + "| " + ret + str(self.id_) + "\n" + "| " + ret + "RET " + str(self.type_) + "\n" +\
               self.compound_instr.printTree(level + 1) + self.body.printTree(level)


    @addToClass(AST.ArgumentsList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.args))

    @addToClass(AST.Argument)
    def printTree(self, level=0):
        return "| " * level  + "ARG " +self.id_ + ": "+ self.type_ + "\n"

    @addToClass(AST.Elements)
    def printTree(self, level=0):
        ret = ""
        for e in self.elements:
            ret += str(e) + "\n"
        return ret


    @addToClass(AST.FunctionDefinition)
    def printTree(self, level=0):
        ret = "| "*level
        ret1 = ret + "| "
        return ret + "FUNDEF\n" + ret1 + str(self.id_) + "\n" + ret1 + "RET " + str(self.type_) + "\n" + self.args_list.printTree(level + 1) + \
               self.compound_instr.printTree(level)
        return ret