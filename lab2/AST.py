class Node(object):

    def __str__(self):
        return self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass



class Float(Const):
    pass



class String(Const):
    pass



class Variable(Node):
    pass



class Program(Node):

    def __init__(self, program_part):
        self.program_parts = []
        self.add_program_part(program_part)

    def add_program_part(self, program_part):
        self.program_parts.append(program_part)



class Declarations(Node):

    def __init__(self, declaration):
        self.declarations = []
        self.add_declaration(declaration)

    def add_declaration(self, declaration):
        self.declarations.append(declaration)



class Declaration(Node):

    def __init__(self, type_, inits):
        self.type_ = type_;
        self.inits = inits;



class Inits(Node):

    def __init__(self, init):
        self.inits = []
        self.add_init(init)

    def add_init(self, init):
        self.add_init(init)



class Init(Node):

    def __init__(self, id_, expression):
        self.id_ = id_;
        self.expression = expression



class Instructions(Node):

    def __init__(self, instruction):
        self.instructions = []
        self.add_instruction(instruction)

    def add_instruction(self, instruction):
        self.instructions.append(instruction)



class Print(Node):

    def __init__(self, expr_list):
        self.expr_list = expr_list



class LabeledInstruction(Node):

    def __init__(self, id_, instruction):
        self.id_ = id_;
        self.instruction = instruction



class Assignment(Node):

    def __init__(self, id_, expression):
        self.id_ = id_
        self.expression = expression



class ChoiceInstruction(Node):

    def __init__(self, condition, instruction, alternate_instruction):
        self.condition = condition
        self.instruction = instruction
        self.alternate_instruction = alternate_instruction



class WhileInstruction(Node):

    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction



class RepeatInstruction(Node):

    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition



class ReturnInstruction(Node):

    def __init__(self, expression):
        self.expression = expression



class ContinueInstruction(Node):
    pass



class BreakInstruction(Node):
    pass



class CompoundInstruction(Node):

    def __init__(self, compound_instr):
        self.compound_instrs = []
        self.add_compound_instr(compound_instr)

    def add_compound_instr(self, compound_instr):
        self.compound_instrs.append(compound_instr)



class GroupedExpression(Node):

    def __init__(self, expression):
        self.expression = expression



class FunctionExpression(Node):

    def __init__(self, id_, expr_list):
        self.id_ = id_
        self.expr_list = expr_list



class ExpressionList(Node):

    def __init__(self, expression):
        self.expressions = []
        self.add_expression(expression)

    def add_expression(self, expression):
        self.expressions.append(expression)



class FunctionsDefinitions(Node):

    def __init__(self, fun_def):
        self.fun_defs = []
        self.add_fun_def(fun_def)

    def add_fun_def(self, fun_def):
        self.fundefs.append(fun_def)



class FunctionDefinition(Node):

    def __init__(self, type_, id_, args_list, compound_instr):
        self.type_ = type_
        self.id_ = id_
        self.args_list = args_list
        self.compound_instr = compound_instr



class ArgumentsList(Node):

    def __init__(self, arg):
        self.args = []
        self.add_arg(arg)

    def add_arg(self, arg):
        self.args.append(arg)



class Argument(Node):

    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


