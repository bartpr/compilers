class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor, args=None):
        if args is None:
            return visitor.visit(self)
        else:
            return visitor.visit(self, args)


class BinExpr(Node):

    def __init__(self, op, left, right, lineNo):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineNo


class Const(Node):
    def __init__(self, lineno, value):
        self.value = value
        self.lineno = lineno


class Integer(Const):
    def __init__(self, lineno, value):
        Const.__init__(self, lineno, value)



class Float(Const):
    def __init__(self, lineno, value):
        Const.__init__(self, lineno, value)


class String(Const):
    def __init__(self, lineno, value):
        Const.__init__(self, lineno, value)

class Variable(Const):
    def __init__(self, lineno, name):
        self.name = name
        self.line = lineno



class Program(Node):

    def __init__(self, elements):
        self.elements = elements



class Elements(Node):

    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)



class Declarations(Node):

    def __init__(self):
        self.declarations = []

    def add_declaration(self, declaration):
        self.declarations.append(declaration)



class Declaration(Node):

    def __init__(self, type_, inits):
        self.type_ = type_;
        self.inits = inits;



class Inits(Node):

    def __init__(self):
        self.inits = []

    def add_init(self, init):
        self.inits.append(init)



class Init(Node):

    def __init__(self, id_, expression, lineno):
        self.id_ = id_;
        self.expression = expression
        self.lineno = lineno



class Instructions(Node):

    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)



class Print(Node):

    def __init__(self, expr_list, lineNO):
        self.expr_list = expr_list
        self.lineNo = lineNO



class LabeledInstruction(Node):

    def __init__(self, id_, instruction):
        self.id_ = id_;
        self.instruction = instruction



class Assignment(Node):

    def __init__(self, id_, expression, lineNO):
        self.id_ = id_
        self.expression = expression
        self.lineno = lineNO



class ChoiceInstruction(Node):

    def __init__(self, id_, condition, instruction, alternate_instruction):
        self.id_ = id_
        self.condition = condition
        self.instruction = instruction
        self.alternate_instruction = alternate_instruction



class WhileInstruction(Node):

    def __init__(self, id_, condition, instruction):
        self.id_ = id_
        self.condition = condition
        self.instruction = instruction



class RepeatInstruction(Node):

    def __init__(self, id_, instructions, condition):
        self.id_ = id_
        self.instructions = instructions
        self.condition = condition



class ReturnInstruction(Node):

    def __init__(self, expression, lineNo):
        self.expression = expression
        self.lineNo = lineNo



class ContinueInstruction(Node):
    def __init__(self, lineNo):
        self.lineNo = lineNo



class BreakInstruction(Node):
    def __init__(self, lineNo):
        self.lineNo = lineNo



class CompoundInstruction(Node):

    def __init__(self, declarations, instructions_opt, endLine):
        self.declarations = declarations
        self.instructions_opt = instructions_opt
        self.endLine = endLine



class FunctionExpression(Node):

    def __init__(self, id_, expr_list, lineno):
        self.id_ = id_
        self.expr_list = expr_list
        self.lineno = lineno



class ExpressionList(Node):

    def __init__(self):
        self.expressions = []

    def add_expression(self, expression):
        self.expressions.append(expression)

    def length(self):
        return len(self.expressions)



class FunctionDefinition(Node):

    def __init__(self, type_, id_, args_list, compound_instr, lineno):
        self.type_ = type_
        self.id_ = id_
        self.args_list = args_list
        self.compound_instr = compound_instr
        self.lineno = lineno



class ArgumentsList(Node):

    def __init__(self):
        self.args = []

    def add_arg(self, arg):
        self.args.append(arg)



class Argument(Node):

    def __init__(self, type_, id_, lineno):
        self.type_ = type_
        self.id_ = id_
        self.lineno = lineno
