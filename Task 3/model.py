class Scope:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def __setitem__(self, key, value):
        self.values[key] = value
    
    def __getitem__(self, key):
        if key in self.values:
            return self.values[key]
            
        if self.parent:
            return self.parent[key]    

class Number:
    def __init__(self, value):
        self.value = value
        
    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        for i, expr in enumerate(self.body):
             if i == len(self.body) - 1:
                return expr.evaluate(scope)
             expr.evaluate(scope)


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

class Conditional:
    def __init__(self, condition, if_true, if_false):
        self.condtion = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if (self.condtion.evaluate(scope).value != 0):
            for i, expr in enumerate(self.if_true):
                if (i == len(self.if_true) - 1):
                    return expr.evaluate(scope)
                expr.evaluate(scope)
        for i, expr in enumerate(self.if_false):
            if (i == len(self.if_false) - 1):
                return expr.evaluate(scope)
            expr.evaluate(scope)         


class Print:
    def __init__(self, expr):
        self.expr = expr
        
    def evaluate(self, scope):
        val = self.expr.evaluate(scope)
        print(val.value)
        return val

class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        val = Number(int(input()))
        scope[self.name] = val 
        return val


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        comp_args = [arg.evaluate(scope) for arg in self.args]
            
        call_scope = Scope(scope)
        for i, arg in enumerate(comp_args):
            call_scope[function.args[i]] = arg
        return function.evaluate(call_scope)

class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.l = lhs
        self.op = op
        self.r = rhs

    def evaluate(self, scope):
        if (self.op == "+"):
            return Number(self.l.evaluate(scope).value + self.r.evaluate(scope).value)
        
        if (self.op == "-"):
            return Number(self.l.evaluate(scope).value - self.r.evaluate(scope).value)

        if (self.op == "*"):
            return Number(self.l.evaluate(scope).value * self.r.evaluate(scope).value)
            
        if (self.op == "/"):
            return Number(self.l.evaluate(scope).value // self.r.evaluate(scope).value)
        
        if (self.op == "%"):
            return Number(self.l.evaluate(scope).value % self.r.evaluate(scope).value)
            
        if (self.op == "=="):
            return Number(int(self.l.evaluate(scope).value == self.r.evaluate(scope).value))
            
        if (self.op == "!="):
            return Number(int(self.l.evaluate(scope).value != self.r.evaluate(scope).value))
       
        if (self.op == "<"):
            return Number(int(self.l.evaluate(scope).value < self.r.evaluate(scope).value))
            
        if (self.op == ">"):
            return Number(int(self.l.evaluate(scope).value > self.r.evaluate(scope).value))
        
        if (self.op == "<="):
            return Number(int(self.l.evaluate(scope).value <= self.r.evaluate(scope).value))
            
        if (self.op == "&&"):
            return Number(int(self.l.evaluate(scope).value and self.r.evaluate(scope).value))
       
        if (self.op == "||"):
            return Number(int(self.l.evaluate(scope).value or self.r.evaluate(scope).value))
            
        return Number(int(self.l.evaluate(scope).value >= self.r.evaluate(scope).value))
                
class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        if (self.op == "-"):
            return Number(-self.expr.evaluate(scope).value)
        return Number(int(self.expr.evaluate(scope).value == 0))

def my_tests():
    testing_input()
    testing_fib()
    testing_abs()
    testing_max()
    testing_linear_equatuion()
    testing_search_scope()
    testing_functions()
    
def testing_input():
    print("Start testing input")    
    print("Write down two integer numbers")
    print("Check: output must contain result of multiply these numbers")
    
    scope = Scope()
    
    i1 = Read('a').evaluate(scope)
    i2 = Read('b').evaluate(scope)
    
    print("Output:", end = ' ')
    Print(BinaryOperation(i1, '*', i2)).evaluate(scope)
    
def testing_fib():
    print("\nStart testing calculating n-th memeber of Fibonacci sequence (zero-numbering)")    
    print("Write down n")
    print("Check: output must contain n-th memeber of Fibonacci sequence")
    
    scope = Scope()
    
    n = Read('n').evaluate(scope)
    print("Output:", end = ' ')
    
    scope['0'] = Number(1)
    scope['1'] = Number(1)
    
    for i in range(2, n.value + 1):
        scope[str(i)] = BinaryOperation(scope[str(i - 1)], '+', scope[str(i - 2)]).evaluate(scope)
    
    Print(scope[str(n.value)]).evaluate(scope)
    

def testing_abs():
    print("\nStart testing geting absolut value of a")    
    print("Write down a")
    print("Check: output must contain abs(a)")

    scope = Scope()
    
    Read('a').evaluate(scope)
    print("Output:", end = ' ')
    scope['zero'] = Number(0)
    
    cond = BinaryOperation(scope['a'], '>', scope['zero'])
    if_true = Print(scope['a'])
    if_false = Print(UnaryOperation('-', scope['a']))
    
    Conditional(cond, [if_true], [if_false]).evaluate(scope)
    
def testing_max():
    print("\nStart testing calculating max of n-element array")    
    print("Write down n then n lines each contains one integer number beq -1000000000")
    print("Check: output must contain maximal element of array")
    
    scope = Scope()
    scope['max'] = Number(-1000000001)
    n = Read('n').evaluate(scope)
    
    for i in range(n.value):
        Read('a').evaluate(scope)
        cond = BinaryOperation(scope['a'], '>', scope['max'])
        if_true = scope['a']
        if_false = scope['max']
        scope['max'] = Conditional(cond, [if_true], [if_false]).evaluate(scope)     
    
    
    print("Output:", end = ' ')
    Print(scope['max']).evaluate(scope)

def testing_linear_equatuion():
    print("\nStart testing calculating solution of linear equatuion")    
    print("Write down a and b where a * x + b have integer solution and a is not equal zero")
    print("Check: output must contain integer solution of this linear equation")
    
    scope = Scope()
    
    Read('a').evaluate(scope)
    Read('b').evaluate(scope)
    print("Output:", end = ' ')
    Print(UnaryOperation('-', BinaryOperation(scope['b'], '/', scope['a']))).evaluate(scope)
    
def testing_search_scope():
    print("\nStart testing scope class")    
    print("Check: output must contain 3")
    print("Output:", end = ' ')
    scope = Scope()
    subscope = Scope(scope)
    subsubscope = Scope(subscope)
    
    scope['a'] = Number(2)
    subscope['b'] = Number(4)
    subsubscope['c'] = Number(3)
    
    Print(BinaryOperation(BinaryOperation(Reference('a'), '+', Reference('b')), '-', Reference('c'))).evaluate(subsubscope)
    
def testing_functions():
    print("\nStart testing functions")    
    print("Check: output must contain 6 and -2 next line")
    print("Output:", end = ' ')
    scope = Scope()
    func = Function(('c', 'd'), [Print(BinaryOperation(Reference('c'), '+', Reference('d'))), Print(BinaryOperation(Reference('c'), '-', Reference('d')))])
    scope['a'] = Number(2)
    scope['b'] = Number(4)
    FunctionCall(FunctionDefinition("func", func), [scope['a'], scope['b']]).evaluate(scope)
        
if __name__ == '__main__':
    my_tests()
