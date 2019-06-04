# Toy - Minha linguagem de programação
Informações a respeito da linguagem no arquivo apresentacao_do_projeto.pdf encontrado no repositório

# Executando o projeto
Criamos um compilador em python para poder executar nossos arquivos .toy
para utilizar clone o repositório e execute 
```
$ python main.py [arquivo de entrada].toy
```
arquivo test.toy disponível para testes no repositório.

# EBNF
```
   program
      : FuncDec
      | VoidDec
      ;
      
   VoidDec
      : 'void', identifier, '(', ')', '\n', { statement, '\n }, 'end', 'void'
      | 'void', identifier, '(', type, identifier, {',', type, identifier} ,')', '\n', {statement, '\n}, 'end', 'void'
      ;
      
   FuncDec
      : 'function', identifier, '(', ')', 'as', type, '\n', { statement, '\n }, 'end', 'function'
      | 'function', identifier, '(', type, identifier, {',', type, identifier} ,')', 'as', type, '\n', {statement, '\n}, 'end', 'function'
      ;   
    
   statement
      : assignment
      | funccall
      | while
      | print
      | declaration
      | if
      ;
   
   assignment
      : identifier, 'is', 'equal', 'to', relExpression
      ;
      
   funccall
      : identifier, '(', ')'
      | identifier, '(', type, identifier, {type, identifier}, ')'
      ;
      
   while
      : 'while', relExpression, '{', {statement, '\n'}, '}'
      ;
      
   print
      : print, relExpression
      ;
      
   declaration
      : type, identifier
      ;
      
   if
      : 'if', relExpression, '{', {statement, '\n'}, '}'
      | 'if', relExpression, '{', {statement, '\n'}, '}', 'else',  '{', {statement, '\n'}, '}'
      ;
      
   type
      : integer
      | boolean
      
   relExpression
      : expression, 'is, 'equal', 'to', expression
      | expression, 'is, 'greater', 'than', expression
      | expression, 'is, 'less', 'than', expression
      ;
      
   expression
      : term, {('plus' | 'minus' | 'or'), term}
      ;
      
   term
      : factor, {('times' | 'divided', 'by' | 'and' ), factor}
      ;
      
   factor
      : '(', relExpression, ')'
      | identifier
      | input
      | boolean
      | integer
      | ('plus' | 'minus' | 'not'), factor
      ;
      
   identifier
      : string, {int,string,'-','_'}
      ;

   string
      : [a-z]+
      ;

   integer
      : [0-9]+
      ;

   boolean
     : 'true'
     | 'false'
     ;
```
