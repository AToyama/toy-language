# toy-language
Computing logic - my language


# EBNF

   statement
      : if
      | print
      | expression
      | for
      | while
      | return
      | break
      | function
      | variable
      ;

   if
     : 'if', comparison, '{', statement, '}'
     | 'if', comparison, '{', statement, '}', 'else', comparison, '{', statement, '}'
     | 'if', comparison, '{', statement, '}', elif, 'else', comparison, '{', statement, '}'
     ;

   elif
     : 'elif', comparison, '{', statement '}'
     ;

   comparison
     : expression, '==', 'expression
     | expression, '>', 'expression
     | expression, '<', 'expression
     | expression, '<=', 'expression
     | expression, '>=', 'expression
     ;

   print
     : '\p', expression
     ;

   for
     :'for',expression,'{', statement, '}'
     ;

   while
     :'while',expression,'{', statement, '}'
     ;

   return
     : '\r', expression
     ;

   break
     : '\b', expression
     ;

   variable
     : name, '=', expression
     ;

   name
     : string, {int,string,'-','_'}
     ;

   function
     : name, '(', arguments, ')', '{', statement, return,'}'
     ;  

   arguments
     : {name,','}
     ;

   expression
     : arithmetics_exp
     | logical_exp
     | unary_exp
     | variable
     ;

   arithmetics_exp
     : expression '+' expression
     | expression '-' expression
     | expression '*' expression
     | expression '/' expression
     | expression '%' expression
     | expression '**' expression
     ;

   logical_exp
     : expression '&' expression
     | expression '|' expression
     | expression '!' expression 
     ;

   unary_exp
     : expression '+'
     | expression '-'
     ;

   string
      : [a-z]+
      ;

   int
      : [0-9]+
      ;

   bool
     : 'True'
     | 'False'
     | 'true'
     | 'false'
     ;
