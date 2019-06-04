# COMPILER PYTHON

# update parser
# mydict.keys()[mydict.values().index(value)]

# v2.3

from node import Node, BinOp, UnOp, IntVal, NoOp, Print, Assignment, Statement, Identifier, Input, While, If, VarDec, Type, BoolVal, Program, FuncDec, VoidDec, FuncCall
from pre_process import PrePro
from symboltable import SymbolTable
from string import ascii_letters, ascii_lowercase
import sys

CHAR = {
    "(" : "OPENP",
    ")" : "CLOSEP",
    "," : "COMMA",
    "{" : "OPENB",
    "}" : "CLOSEB",
}

RESERVED = ['is','equal','to','plus','minus','times','divided','by','greater','less','than','function','input','print','begin','end','and','or','not','while','wend','if','then','else','dim','true','false','void','as','boolean','integer']

VARNAME_CHARS = '0123456789_' + ascii_letters

class Token():

    def __init__(self, tp, value):
        self.tp = tp
        self.value = value

class Tokenizer():

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self): 

        eof = True

        # Tokenize the expression
        if self.position < len(self.origin): 
            eof = False

        # ignore spaces
        if not eof:
            while self.origin[self.position] == " ":
                self.position += 1
                if self.position == len(self.origin):
                    eof = True
                    break  
            
        if not eof:
            if self.origin[self.position].isdigit():
                
                num = ""
    
                while self.origin[self.position].isdigit():

                    num += self.origin[self.position]
                    self.position += 1

                    if self.position  == len(self.origin):
                        break
                    
                token = Token("INT",int(num))

            elif self.origin[self.position] in CHAR:

                token = Token(CHAR[self.origin[self.position]],self.origin[self.position])
                self.position += 1
            
            elif self.origin[self.position] == "\n":
                token = Token("BREAK_LINE","\\n")
                self.position += 1

            elif self.origin[self.position].isalpha():
                    
                aux = ""

                while self.origin[self.position] in VARNAME_CHARS:

                    aux += self.origin[self.position]
                    self.position += 1
                
                    if self.position  == len(self.origin):
                        break

                if aux in RESERVED:
                    token = Token(aux.upper(),aux)

                else:
                    token = Token("IDENTIFIER", aux)

            else:

                # Invalid Token
                raise ValueError(f"{self.origin[self.position]} is not a number")   

        # End of File 
        else:

            token = Token("EOF", None)

        self.actual = token

        # print(self.actual.tp,self.actual.value)


class Parser():

    tokens = None

    @staticmethod
    def run(source):

        source = PrePro.filter(source)
        Parser.tokens = Tokenizer(source)
        Parser.tokens.selectNext()

        st = SymbolTable(None)

        Parser.program().Evaluate(st)
        
        if Parser.tokens.actual.tp != "EOF":
            raise ValueError(f"{Parser.tokens.actual.value} invalid at end of sentence")

    def parseFactor():

        #Parser.tokens.selectNext()

        if Parser.tokens.actual.tp == "INT":
            node = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "PLUS":
            Parser.tokens.selectNext()
            node = UnOp("+",Parser.parseFactor())

        elif Parser.tokens.actual.tp == "MINUS":
            Parser.tokens.selectNext()
            node = UnOp("-",Parser.parseFactor())
        
        elif Parser.tokens.actual.tp == "NOT":
            Parser.tokens.selectNext()
            node = UnOp("NOT",Parser.parseFactor())

        elif Parser.tokens.actual.tp in ["TRUE","FALSE"]:
            node = BoolVal(Parser.tokens.actual.tp)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "OPENP":
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()

            if Parser.tokens.actual.tp != "CLOSEP":
                raise ValueError("Missing parentheses")
            else:
                Parser.tokens.selectNext()
        
        elif Parser.tokens.actual.tp == "IDENTIFIER":
            var_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.tp == "OPENP":
                parameters = []
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    parameters.append(Parser.parseRelExpression())
                    
                    if Parser.tokens.actual.tp == "COMMA":
                        Parser.tokens.selectNext()

                    else:
                        break

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise ValueError("Missing parentheses")
                node = FuncCall(var_name,parameters)
                Parser.tokens.selectNext()           

            else:
                node = Identifier(var_name)            

        elif Parser.tokens.actual.tp == "INPUT":
            node = Input()
            Parser.tokens.selectNext()

        else:
            raise ValueError(f"{Parser.tokens.actual.value} not a valid operator")

        return node


    def parseTerm():

        node = Parser.parseFactor()

        while Parser.tokens.actual.tp in ["DIVIDED","TIMES","AND"]:
            
            if Parser.tokens.actual.tp == "TIMES":
                Parser.tokens.selectNext()
                node = BinOp("*",[node,Parser.parseFactor()])

            elif Parser.tokens.actual.tp == "DIVIDED":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tp == "BY":   
                    Parser.tokens.selectNext()
                    node = BinOp("/",[node,Parser.parseFactor()])
                
                else:
                  raise ValueError("to do a division must write divided by")

            elif Parser.tokens.actual.tp == "AND":
                Parser.tokens.selectNext()
                node = BinOp("AND",[node,Parser.parseFactor()])

        return node


    def parseExpression():

        node = Parser.parseTerm()

        while Parser.tokens.actual.tp in ["PLUS","MINUS","OR"]:

            if Parser.tokens.actual.tp == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "OR":
                Parser.tokens.selectNext()
                node = BinOp("OR",[node,Parser.parseTerm()])

        return node

    def parseRelExpression():

        node = Parser.parseExpression()

        if Parser.tokens.actual.tp == "IS":
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp in ["EQUAL","GREATER","LESS"]:

                if Parser.tokens.actual.tp == "EQUAL":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "TO":
                        node = BinOp("=",[node,Parser.parseExpression()])

                elif Parser.tokens.actual.tp == "GREATER":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "THAN":
                        Parser.tokens.selectNext()
                        node = BinOp(">",[node,Parser.parseExpression()])

                elif Parser.tokens.actual.tp == "LESS":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "THAN":
                        Parser.tokens.selectNext()
                        node = BinOp("<",[node,Parser.parseExpression()])

        return node

    def parseType():

        if Parser.tokens.actual.tp == "INTEGER":
            Parser.tokens.selectNext()
            node = Type("INTEGER")

        elif Parser.tokens.actual.tp == "BOOLEAN":
            Parser.tokens.selectNext() 
            node = Type("BOOLEAN")
            
        else:
            raise ValueError("variable type not supported")

        return node

    def parseStatement():

        if Parser.tokens.actual.tp == "IDENTIFIER":
            variable_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
    
            if Parser.tokens.actual.tp == "IS":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tp == "EQUAL":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "TO":
                        Parser.tokens.selectNext()
                        node = Assignment([Identifier(variable_name), Parser.parseRelExpression()])

            elif Parser.tokens.actual.tp == "OPENP":
                parameters = []
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    parameters.append(Parser.parseRelExpression())
                    
                    if Parser.tokens.actual.tp == "COMMA":
                        Parser.tokens.selectNext()

                    else:
                        break

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise ValueError("Missing parentheses")

                node = FuncCall(variable_name,parameters)
                Parser.tokens.selectNext()

            else:
                raise ValueError(f"EQUAL token expected, got {Parser.tokens.actual.tp}")

        
        elif Parser.tokens.actual.tp == "PRINT":
            Parser.tokens.selectNext()
            node = Print(Parser.parseRelExpression())

        elif Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
            variable_type = Parser.parseType()

            if Parser.tokens.actual.tp == "IDENTIFIER":
                variable_name = Identifier(Parser.tokens.actual.value)        
                node = VarDec([variable_name, variable_type])
                Parser.tokens.selectNext()
                
            else:
              raise ValueError(f"IDENTIFIER expected, got {Parser.tokens.actual.tp}")

        elif Parser.tokens.actual.tp == "WHILE":

            Parser.tokens.selectNext()
            condition = Parser.parseRelExpression()
            
            if Parser.tokens.actual.tp == "OPENB":
                Parser.tokens.selectNext()
                statements = []

                while Parser.tokens.actual.tp != "CLOSEB":
                    statements.append(Parser.parseStatement())

                    if Parser.tokens.actual.tp == "BREAK_LINE":
                        Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                Parser.tokens.selectNext()
                node = While([condition, statements])

            else:
                raise SyntaxError(f"must skip a line after while condition")

        elif Parser.tokens.actual.tp == "IF":
            
            Parser.tokens.selectNext()
            condition = Parser.parseRelExpression()
            
            if Parser.tokens.actual.tp == "OPENB":
                Parser.tokens.selectNext()
                
                if_statements = []

                while Parser.tokens.actual.tp != "CLOSEB":

                    if_statements.append(Parser.parseStatement())

                    if Parser.tokens.actual.tp == "BREAK_LINE":
                        Parser.tokens.selectNext()
                    
                    else:
                        raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                if Parser.tokens.actual.tp != "CLOSEB":
                    raise ValueError(f"CLOSEB expected, got {Parser.tokens.actual.tp}")
          
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()
          
                if Parser.tokens.actual.tp == "ELSE":
                    Parser.tokens.selectNext()
                    
                    if Parser.tokens.actual.tp == "OPENB":
                        Parser.tokens.selectNext()
                    
                        else_statements = []

                        while Parser.tokens.actual.tp != "CLOSEB":
                            else_statements.append(Parser.parseStatement())

                            if Parser.tokens.actual.tp == "BREAK_LINE":
                                Parser.tokens.selectNext()
                        
                            else:
                                raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                        if Parser.tokens.actual.tp != "CLOSEB":
                            raise ValueError(f"CLOSEB expected, got {Parser.tokens.actual.tp}")
                        
                        node = If([condition,if_statements,else_statements])
                        Parser.tokens.selectNext()
                
                else:
                    node = If([condition,if_statements])

            else:
                raise SyntaxError(f"OPENB token expected, got {Parser.tokens.actual.value}")
        else:
            return NoOp(None)

        return node 

    def funcDec():

        statements = []
        parameters = []

        if Parser.tokens.actual.tp == "IDENTIFIER":
            
            func_name = Parser.tokens.actual.value

            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "OPENP":
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    
                    if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                        var_type = Parser.tokens.actual.tp
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.tp == "IDENTIFIER":

                            parameters.append((Parser.tokens.actual.value, var_type))
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.tp == "COMMA":
                                Parser.tokens.selectNext()
                            else:
                                break

                        else:
                            raise SyntaxError(f"IDENTIFIER token expected, got {Parser.tokens.actual.value}")

                    else:
                        raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise SyntaxError(f"CLOSEP token expected, got {Parser.tokens.actual.value}")

                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "AS":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                        func_type = Parser.tokens.actual.tp
                        Parser.tokens.selectNext()

                    else:
                        raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")
                
                else:
                    raise SyntaxError(f"AS token expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.tp != "END":
                        statements.append(Parser.parseStatement())

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                        else:
                          raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "FUNCTION":
                        Parser.tokens.selectNext()

                        while Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"FUNCTION expected, got {Parser.tokens.actual.tp}")
                else:
                    raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                return FuncDec([(func_name, func_type),parameters,statements])

            else:
                raise SyntaxError(f"OPENP token expected, got {Parser.tokens.actual.value}")


    def voidDec():

        statements = []
        parameters = []

        if Parser.tokens.actual.tp == "IDENTIFIER":
            
            void_name = Parser.tokens.actual.value

            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "OPENP":
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    
                    if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                        var_type = Parser.tokens.actual.tp
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.tp == "IDENTIFIER":

                            parameters.append((Parser.tokens.actual.value, var_type))
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.tp == "COMMA":
                                Parser.tokens.selectNext()
                            else:
                                break

                        else:
                            raise SyntaxError(f"IDENTIFIER token expected, got {Parser.tokens.actual.value}")

                    else:
                        raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise SyntaxError(f"CLOSEP token expected, got {Parser.tokens.actual.value}")

                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.tp != "END":
                        statements.append(Parser.parseStatement())

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()
                        
                        elif Parser.tokens.actual.tp == "END":
                            break

                        else:
                          raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "VOID":
                        Parser.tokens.selectNext()

                        while Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"VOID expected, got {Parser.tokens.actual.tp}")
                else:
                    raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
           
                return VoidDec([void_name , parameters, statements])

            else:
                raise SyntaxError(f"OPENP token expected, got {Parser.tokens.actual.value}")


    def program():

        statements = []

        while Parser.tokens.actual.tp == "BREAK_LINE":
            Parser.tokens.selectNext()

        while Parser.tokens.actual.tp in ["VOID","FUNCTION"]:
            
            if Parser.tokens.actual.tp == "VOID":
                Parser.tokens.selectNext()
                statements.append(Parser.voidDec())

            else:
                Parser.tokens.selectNext()
                statements.append(Parser.funcDec())

        statements.append(FuncCall("main",[]))

        return Program(statements)

with open(sys.argv[1], 'r') as myfile:
    source = myfile.read()
#print(source)

Parser.run(source)