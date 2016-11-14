import AST

LEVEL_TOKEN = "| "

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        return  "| " * level + self.op + "\n" + self.left.printTree(level + 1) + self.right.printTree(level + 1)

    @addToClass(AST.Const)
    def printTree(self, level=0):

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
        return self.program_parts.printTree()

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
        ret = ret + str(self.id) + "\n" + str(self.val)
        return ret

    @addToClass(AST.Instructions)
    def printTree(self):
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
        return "| " * level + "=\n" + "| "  * (level + 1) + str(self.id_) + "\n" + self.expr.printTree(indent + 1)

