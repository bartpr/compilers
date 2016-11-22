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
        return  "| " * level + self.op + "\n" + self.left.printTree(level + 1)+ '\n' + self.right.printTree(level + 1)

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
    def printTree(self, level = 0):
        ret = ""
        x = ""
        for d in self.declarations:
            ret += x + d.printTree(level)
            x = "\n"
        return ret

    @addToClass(AST.Declaration)
    def printTree(self, level=0):
        ret = "| " * level
        ret = ret + "DECL\n" + ("" if self.inits is None else self.inits.printTree(level + 1))
        return ret

    @addToClass(AST.Inits)
    def printTree(self, level=0):
        ret = "| " * level
        retu = ""
        x = ""
        for i in self.inits:
            retu += x + ret + "=\n" + i.printTree(level+1)
            x = "\n"
        return retu

    @addToClass(AST.Init)
    def printTree(self, level = 0):
        ret = "| " * level
        ret = ret + str(self.id_) + "\n"+ ret + str(self.expression)
        return ret

    @addToClass(AST.Instructions)
    def printTree(self, level = 0):
        ret = ""
        x = ""
        for i in self.instructions:
            ret += x + i.printTree(level)
            x = "\n"
        return ret

    @addToClass(AST.Print)
    def printTree(self, level=0):
        ret = "| " * level
        ret += "PRINT\n" + self.expr_list.printTree(level + 1)
        return ret


    @addToClass(AST.LabeledInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "LABEL\n" + "| " *(1+level) + str(self.id) + "\n" + self.instruction.printTree(level + 1)

    @addToClass(AST.Assignment)
    def printTree(self, level=0):
        return "| " * level +"=\n" + "| "  * (level + 1) + str(self.id_) + "\n" + self.expression.printTree(level +1 )


    @addToClass(AST.WhileInstruction)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "WHILE\n" + self.condition.printTree(level + 1) + "\n" + self.instruction.printTree(level + 1)


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
         if self.declarations is None:
            ret = ""
         else:
            ret = self.declarations.printTree(level) + "\n"
         return ret + ("" if self.instructions_opt is None else self.instructions_opt.printTree(level))


    @addToClass(AST.ExpressionList)
    def printTree(self, level=0):
        ret = ""
        x = ""
        for e in self.expressions:
            ret += x + e.printTree(level)
            x = "\n"
        return ret


    @addToClass(AST.FunctionExpression)
    def printTree(self, level=0):
        ret = "| " * level
        return ret + "FUNCALL\n" + "| " + ret + str(self.id_) + "\n" + self.expr_list.printTree(level + 1) + "\n"


    @addToClass(AST.ArgumentsList)
    def printTree(self, level=0):
        return "".join(map(lambda x: x.printTree(level), self.args))

    @addToClass(AST.Argument)
    def printTree(self, level=0):
        return "| " * level  + "ARG " +self.id_ + "\n"

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
               self.compound_instr.printTree(level + 1)
        return ret

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, level=0):

        ret = "| " * level

        if self.alternate_instruction is None:
            ret +=  "IF\n" + self.condition.printTree(level+1) + "\n" + self.instruction.printTree(level + 1)
        else:
            ret +=  "IF\n" + self.condition.printTree(level + 1) + "\n" + self.instruction.printTree(level + 1) + ret + "ELSE\n" + self.alternate_instruction.printTree(level + 1)
        return ret
