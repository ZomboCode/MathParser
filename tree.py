import math
#global variables
funcs = {"log10":math.log10, "sin":math.sin, "cos":math.cos, "ln":math.log,
         "sqrt":math.sqrt, "tan":math.tan, "cot":math.cos, "acos":math.acos,
         "asin":math.asin, "atan":math.atan, "ceil":math.ceil, "floor":math.floor}


ops = {"+":0, "-":0, "*":2, "/":2, "^":3, "**":3, "(":-1, ")":-1}
order = {"+":0, "-":0, "*":0, "/":0, "^":1, "**":1, "(":0, ")":0}

def is_num(text):
    try:
        float(text)
        return True
    except:
        return False

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
        if self.mode == "binary": #do some (but not all possible) simplifications
            #print(self.children[0].children, self.func, self.children[1].children[0])
            if is_num(self.children[0].children[0]) and is_num(self.children[1].children[0]):
                self.children = [operate(self.children[0].children[0], self.children[1].children[0], self.func)]
                self.func = "return"
                self.mode = "single"

            elif is_num(self.children[0].children[0]) and self.children[0].children[0] == 0:
                if self.func == "*" or self.func == "/" or self.func == "**":
                    self.children = [0]
                    self.func = "return"
                    self.mode = "single"
                if self.func == "+" or self.func == "-":
                    self.func = self.children[1].func
                    self.mode = self.children[1].mode
                    self.children = [self.children[1]]
                

            elif is_num(self.children[1].children[0]) and self.children[1].children[0] == 0:
                if self.func == "*" or self.func == "**":
                    self.children = [0]
                    self.func = "return"
                    self.mode = "single"
                if self.func == "+" or self.func == "-":
                    self.func = self.children[0].func
                    self.mode = self.children[0].mode
                    self.children = self.children[0].children

                if self.func == "/":
                    self.children = [math.inf]
                    self.func = "return"
                    self.mode = "single"
                  
    def printTree(self):
        if self.func != "return":
            print(self.func)
            for child in self.children:
                child.printTree()    
        else:
            print(self.children[0])

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

    def derivative(self):
        if self.mode == "binary":
            if self.func == "+" or self.func == "-":
                return Tree("binary", self.func, [self.children[0].derivative(), self.children[1].derivative()])
            if self.func == "*":
                a = Tree("binary", "*", [self.children[0], self.children[1].derivative()])
                b = Tree("binary", "*", [self.children[0].derivative(), self.children[1]])
                return Tree("binary", "+", [a, b])
            
            if self.func == "/":
                a = Tree("binary", "*", [self.children[0], self.children[1].derivative()])
                b = Tree("binary", "*", [self.children[0].derivative(), self.children[1]])
                c = Tree("binary", "-", [b, a])
                d = Tree("binary", "*", [self.children[1], self.children[1]])
                return Tree("binary", "/", [c, d])
            
            if self.func == "**":
                if (self.children[0].func == "return" and self.children[0].children[0] == "x" and
                    self.children[1].func == "return" and is_num(self.children[1].children[0])):
                    a = Tree("binary", "**", [self.children[0], Tree("single", "return", [self.children[1].children[0] - 1])])
                    a.printTree()
                    return Tree("binary", "*", [Tree("single", "return", [self.children[1].children[0]]), a]) 
                else:
                    return self
                
        elif self.mode == "single":
            if self.func == "return":
                if self.children[0] == "x":
                    return Tree("single", "return", [1])
                else:
                    return Tree("single", "return", [0])
        
    def intergral(self, a, b, step):
        ans = 0
        a = step/2
        while a < b:
            ans += self.calculate(a) * step
            a += step

        return ans
            
            