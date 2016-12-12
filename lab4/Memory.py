

class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.dictonary = {}
        pass

    def has_key(self, name):  # variable name
        return name in self.dictonary

    def get(self, name):  # gets from memory current value of variable <name>
        return self.dictonary.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.dictonary[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = []
        if memory is not None:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("top"))

    def get(self, name):  # gets from memory stack current value of variable <name>
        indices = reversed(range(len(self.stack)))
        for i in indices:
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        indices = reversed(range(len(self.stack)))
        for i in indices:
            if self.stack[i].has_key(name):
                self.stack[i].put(name, value)
                break

    def peek(self):
        return self.stack[-1]

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()



class FunctionMemoryStack:
    def __init__(self, stack=None):  # initialize memory stack with memory <memory>
        self.stack = []
        if stack is not None:
            self.stack.append(stack)
        else:
            self.stack.append(MemoryStack())

    def in_fun(self):
        return len(self.stack) > 1;

    def push(self, stack):  # pushes memory <memory> onto the stack
        self.stack.append(stack)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]