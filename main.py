import math
from collections import deque

funcs = {"log10":math.log10, "sin":math.sin, "cos":math.cos, "ln":math.log,
         "sqrt":math.sqrt, "tan":math.tan, "cot":math.cos, "acos":math.acos,
         "asin":math.asin, "atan":math.atan, "ceil":math.ceil, "floor":math.floor}

ops = {"+":0, "-":0, "*":2, "/":2, "^":3, "(":-1, ")":-1}
order = {"+":0, "-":0, "*":0, "/":0, "^":1, "(":0, ")":0}

class Tree:
    def __init__(self, mode, func, children):
        self.mode = mode
        self.func = func
        self.children = children

    def calculate(self, x):
        if self.mode == "binary":
            a = self.calculate(self.children[0], x)
            b = self.calculate(self.children[1], x)
            if self.func == "+":
                return a + b
            if self.func == "-":
                return a - b
            if self.func == "*":
                return a * b
            if self.func == "/":
                if (b == 0): b = 0.1; a = math.inf
                return a / b
            if self.func == "**":
                return a ** b

        elif self.mode == "single":
            if self.func == "return":
                if (self.children[0] == "x"):
                    return x
                return self.children[0]
            
            
            for func in funcs:
                if func == self.func:
                    funcs[func](self.children[0])

#toTree(2+(3*x)**4 + x/5 - x)
def is_num(text):
    try:
        float(text)
        return True
    except:
        return False
    

def appendStack(stack, output, c):
    while(len(stack) > 0):
        op = 4
        if (stack[-1] in ops):
            op = ops[stack[-1]]
        if (op > ops[c] or (op == ops[c] and order[c] == 0)):
            output.append(stack.pop())
        else:
            break
    stack.append(c)
    return stack, output




def parser(text):
    curr = ""
    curr_num = False
    stack = deque()
    output = []
    
    error = ""
    text = text.replace(" ", "")

    print(text)
    for i in range(len(text)):
        c = text[i]

        curr += c
        if (is_num(curr)):
            curr_num = True
            if i == (len(text) - 1):
                output.append(float(curr))
        elif (curr_num == True):
            output.append(float(curr[:-1]))
            if (c not in ops or (c in ops and (c == "("))):
                stack, output = appendStack(stack, output, "*")
            curr = c
            curr_num = False
        

        if c == "(":
            stack.append(c)
            curr = ""

        elif c == ")":
            while(len(stack) > 0 and stack[-1] != "("):
                output.append(stack.pop())
            
            if (len(stack) != 0):
                stack.pop()
            else:
                error = "Parenthesis error"
            curr = ""

        elif c in ops:
            stack, output = appendStack(stack, output, c)
            
            curr = ""
        
        elif curr in funcs:
            print(curr)
            stack.append(curr)
            curr = ""
    

    while (len(stack) > 0):
        output.append(stack.pop())
    
    if error != "":
        print("WARNING!")
        print(error)
    else:
        print(output)
    



parser("3.5 + 4 * 2 / 5sin 1 - 5 ^ 2 ^ 3")
parser("5(sin(8*5-3))")

            
            






    


