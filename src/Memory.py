

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):         # gets from memory current value of variable <name>
        return self.variables.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory is None:
            memory = Memory("global")
        self.stack = [memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name, value)
                return
        self.stack[-1].put(name, value)  # insert into global memory if not found

    def set(self, name, value): # sets variable <name> to value <value>
        self.stack[-1].put(name, value)

    def push(self, memory_name): # pushes memory <memory> onto the stack
        self.stack.append(Memory(memory_name))

    def pop(self):          # pops the top memory from the stack
        popped = self.stack.pop()
        for key, value in popped.variables.items():
            for memory in reversed(self.stack):
                if memory.has_key(key):
                    memory.put(key, value)
                    break


