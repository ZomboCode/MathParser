import math
#global variables
funcs = {"log10":math.log10, "sin":math.sin, "cos":math.cos, "ln":math.log,
         "sqrt":math.sqrt, "tan":math.tan, "cot":math.cos, "acos":math.acos,
         "asin":math.asin, "atan":math.atan, "ceil":math.ceil, "floor":math.floor}

ops = {"+":0, "-":0, "*":2, "/":2, "^":3, "**":3, "(":-1, ")":-1}
order = {"+":0, "-":0, "*":0, "/":0, "^":1, "**":1, "(":0, ")":0}

def operate(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if (b == 0): b = 0.1; a = math.inf
        return a / b
    if op == "^" or op == "**":
        if (b - math.floor(b) == 0):
            return a ** b
        else:
            return math.inf

#tree to evaluate function
class Tree:
    def __init__(self, mode, func, children):
        self.mode = mode
        self.func = func
        self.children = children

    def calculate(self, x):
        if self.mode == "binary":
            a = self.children[0].calculate(x)
            b = self.children[1].calculate(x)
            return operate(a, b, self.func)

        elif self.mode == "single":
            if self.func == "return":
                if (self.children[0] == "x"):
                    return x
                return self.children[0]
            
            if self.func in funcs:
                return funcs[self.func](self.children[0].calculate(x))