from tree import *
from collections import deque
#check if string is float
def is_num(text):
    try:
        float(text)
        return True
    except:
        return False
    
#add operator to stack and do changes
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

#Shunting-yard algorithm
def parser(text):
    curr = ""
    curr_num = False
    was_num = False
    curr_sign = 1
    stack = deque()
    output = []
    error = ""
    text = text.replace(" ", "")

    space_funcs = {}
    for func in funcs:
        ids = [index for index in range(len(text))
               if text.startswith(func, index)]
        for i in ids:
            space_funcs[i] = func
    
    print(text)
    i = -1
    while i < len(text)-1:
        i += 1
        c = text[i]

        if i in space_funcs: #if index i is function
            stack.append(space_funcs[i])
            i += len(space_funcs[i])-1
        else: #index i is is not function
            curr += c
            if is_num(curr):
                curr_num = True
                if i == (len(text) - 1):
                    output.append(float(curr)*curr_sign)
            elif curr_num == True:
                if (len(curr) > 1):
                    output.append(float(curr[:-1])*curr_sign)
                    curr_sign = 1
                
                if c == "x":
                    output.append("x")

                if c not in ops or (c in ops and (c == "(")):
                    stack, output = appendStack(stack, output, "*")
                
                if (c != "x"):
                    curr_num = False
                    curr = c
                else:
                    curr = ""

            elif c == "x":
                curr_num = True
                output.append("x")
                curr = ""

            

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
                if i != len(text)-1 and c == "*" and text[i+1] == "*":
                    c = "**"
                    i += 1
                
                if c == "-" and (not was_num and not text[i-1] == ")"):
                    curr_sign *= -1
                elif c == "+" and (not was_num and not text[i-1] == ")"):
                    pass
                else:
                    stack, output = appendStack(stack, output, c)
                curr = ""

        was_num = curr_num
                
                        
    
    #empty stack
    while (len(stack) > 0):
        output.append(stack.pop())
    
    if error != "":
        print("WARNING!")
        print(error)
    else:
        print(output)
    return output


#evaluates expression in RPN wih give
def blitzkrieg(arr, x):
    error = ""
    ansStack = deque()
    for i in arr:
        if i == "x":
            ansStack.append(x)
        elif is_num(i):
            ansStack.append(float(i))
        elif i in ops:
            a = operate(ansStack[-2], ansStack[-1], i)
            if a == math.inf:
                error = "Tried taking root of negative number"
                break
            ansStack.pop()
            ansStack.pop()
            ansStack.append(a)

        elif i in funcs:
            a = funcs[i](ansStack[-1])
            ansStack.pop()
            ansStack.append(a)

    if error != "":
        print("WARNING")
        print(error)
    else:
        print(ansStack[0])

#builds tree from reverse polish notation
def blitzkriegToTree(arr, x):
    ansStack = deque()
    for i in arr:
        if i == "x":
            ansStack.append(Tree("single", "return", ["x"]))
        elif is_num(i):
            ansStack.append(Tree("single", "return", [float(i)]))
        elif i in ops:
            a = Tree("binary", i, [ansStack[-2], ansStack[-1]])
            ansStack.pop()
            ansStack.pop()
            ansStack.append(a)
        elif i in funcs:
            a = Tree("single", i, [ansStack[-1]])
            ansStack.pop()
            ansStack.append(a)
    
    print(ansStack[0].calculate(2))
            

    

sx = parser("3 + 4 * 2 / (1-5) ** 2.5 * 3")
blitzkrieg(sx, 2)
blitzkriegToTree(sx, 2)

sy = parser("sin(5x**2)-5/9")
blitzkrieg(sy, 2)
blitzkriegToTree(sy, 2)