from symboltable import SymbolTable

class Node():

    def __init__(self):

        value = None
        children = []

    def Evaluate(self, symboltable):
        pass

class BinOp(Node):

    def __init__(self, value, children):

        self.value = value
        self.children = children

    def Evaluate(self, symboltable):

        if self.value == "+":
            return self.children[0].Evaluate(symboltable) + self.children[1].Evaluate(symboltable)
            
        elif self.value == "-":
            return self.children[0].Evaluate(symboltable) - self.children[1].Evaluate(symboltable)

        elif self.value == "*":
            return self.children[0].Evaluate(symboltable) * self.children[1].Evaluate(symboltable)

        elif self.value == "/":
            return self.children[0].Evaluate(symboltable) // self.children[1].Evaluate(symboltable)

        elif self.value == ">":
            return self.children[0].Evaluate(symboltable) > self.children[1].Evaluate(symboltable)
        
        elif self.value == "<":
            return self.children[0].Evaluate(symboltable) < self.children[1].Evaluate(symboltable)

        elif self.value == "=":
            return self.children[0].Evaluate(symboltable) == self.children[1].Evaluate(symboltable)

        elif self.value == "AND":
            return self.children[0].Evaluate(symboltable) and self.children[1].Evaluate(symboltable)

        elif self.value == "OR":
            return self.children[0].Evaluate(symboltable) or self.children[1].Evaluate(symboltable)

class UnOp(Node):

    def __init__(self, value, children):

      self.value = value
      self.children = children

    def Evaluate(self, symboltable):

        if self.value == "+":
            return self.children.Evaluate(symboltable)
        
        elif self.value == "-":
            return - self.children.Evaluate(symboltable)
        
        elif self.value == "NOT":
            return not self.children.Evaluate(symboltable)

class IntVal(Node):

    def __init__(self, value):

        self.value = value

    def Evaluate(self, symboltable):

        return self.value

class NoOp(Node):

    def __init__(self, value):
        self.value = None

class Print(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):
        print(self.children.Evaluate(symboltable))

class Assignment(Node):

    def __init__(self, children):

        self.children = children

    def Evaluate(self, symboltable):
        # print(self.children[1].Evaluate(symboltable),"DEBUGG")
        symboltable.setter(self.children[0].value, self.children[1].Evaluate(symboltable))
        # print(symboltable.symbol_table,"DEBUG")

class Identifier(Node):
    
    def __init__(self, value):      
        self.value = value

    def Evaluate(self, symboltable):
        # print(self.value, symboltable.symbol_table)
        return symboltable.getter(self.value)[0]

class Statement(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        for child in self.children:
            child.Evaluate(symboltable)

class Input(Node):

    #def __init__(self, value):
        
    #    self.value = value
    
    def Evaluate(self, symboltable):

        return int(input())

class If(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        if self.children[0].Evaluate(symboltable):
            for child in self.children[1]:
                child.Evaluate(symboltable)
        else:
            if len(self.children) == 3:
                for child in self.children[2]:
                    child.Evaluate(symboltable)

class While(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):
    
        while self.children[0].Evaluate(symboltable):
            
            for child in self.children[1]:
                child.Evaluate(symboltable)

class Type(Node):
    
    def __init__(self, value):
        
        self.value = value    

    def Evaluate(self, symboltable):

        return self.value

class BoolVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, st):
        
        if self.value == "TRUE":
            return True

        elif self.value == "FALSE":
            return False

class VarDec(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        st.declare(self.children[0].value, self.children[1].Evaluate(st))

class Program(Node):
    
    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class FuncDec(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        st.create(self.children[0][0],self,"FUNCTION")

class VoidDec(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        st.create(self.children[0],self,"VOID")

class FuncCall(Node):

    def __init__(self, value, children):
        self.children = children
        self.value = value
    
    def Evaluate(self, st):

        new_st = SymbolTable(st)
        get_node = st.getter(self.value)
        node = get_node[0]
        func_void = get_node[1]
        
        if func_void == "FUNCTION":
            new_st.declare(node.children[0][0],node.children[0][1])
        
        if node.children:
            if len(self.children) > len(node.children[1]):
                raise ValueError(f"Too many arguments in {self.value}")

            if len(self.children) < len(node.children[1]):
                raise ValueError(f"missing arguments in {self.value}")

        for i in range(len(node.children[1])):
            new_st.create(node.children[1][i][0],self.children[i].Evaluate(st),node.children[1][i][1])
       
        for child in node.children[2]:
            child.Evaluate(new_st)

        if func_void == "FUNCTION":
            return_value = new_st.getter(self.value)
            # print(return_value)
            
            #if the type match
            if return_value[1] == node.children[0][1]:
                return return_value[0]