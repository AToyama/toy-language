// based on  https://gnuu.org/2009/09/18/writing-your-own-toy-compiler/

%{
  #include <stdio.h>
  int yylex (void);
  void yyerror (char const *);
%}

%token
BREAK_LINE IDENTIFIER DOUBLE_EQUALINTEGER FLOAT EQUAL DOUBLE_EQUAL NOT_EQUAL LT LET GT GET OPEN_BRACE OPEN_PARENT CLOSE_BRACE CLOSE_PARENT DOT COMMA PLUS MINUS MULT DIV AND OR NOT INC DEC MULT_EQUAL DIV_EQUAL PLUS_EQUAL MINUS_EQUAL PRINT RETURN BREAK WHILE IF ELSE ELIF DEF FOR


%%

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
     : IF comparison OPEN_BRACE statement CLOSE_BRACE
     | IF comparison OPEN_BRACE statement CLOSE_BRACE ELSE comparison OPEN_BRACE statement CLOSE_BRACE
     | IF comparison OPEN_BRACE statement CLOSE_BRACE elif ELSE comparison OPEN_BRACE statement CLOSE_BRACE
     ;

   elif
     : ELIF comparison OPEN_BRACE statement CLOSE_BRACE
     ;

   comparison
     : expression DOUBLE_EQUAL expression
     | expression NOT_EQUAL expression
     | expression GT expression
     | expression LT expression
     | expression GET expression
     | expression LET expression
     ;

   print
     : PRINT expression BREAK_LINE
     ;

   for
     :FOR expression OPEN_BRACE statement CLOSE_BRACE
     ;

   while
     : WHILE expression OPEN_BRACE statement CLOSE_BRACE
     ;

   return
     : RETURN expression BREAK_LINE
     ;

   break
     : BREAK BREAK_LINE
     ;

   variable
     : IDENTIFIER EQUAL expression
     ;

   function
     : IDENTIFIER OPEN_PARENT arguments CLOSE_PARENT OPEN_BRACE statement return CLOSE_BRACE
     ;  

   arguments
     : { IDENTIFIER COMMA }
     ;

   expression
     : arithmetics_exp
     | logical_exp
     | unary_exp
     | variable
     ;

   arithmetics_exp
     : expression PLUS expression
     | expression MINUS expression  
     | expression MULT expression
     | expression DIV expression
     ;

   logical_exp
     : expression AND expression
     | expression OR expression
     | expression NOT expression 
     ;

   unary_exp
     : expression PLUS
     | expression MINUS
     ;

%%