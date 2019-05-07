// based on  https://gnuu.org/2009/09/18/writing-your-own-toy-compiler/


%{
#include <string>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

%%

[ \t\n]                 return TOKEN(BREAK_LINE)
[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return IDENTIFIER;
[0-9]+.[0-9]*           SAVE_TOKEN; return DOUBLE;
[0-9]+                  SAVE_TOKEN; return INTEGER;
[0-9]*\.[0-9]+          SAVE_TOKEN; return FLOAT;
"="                     return TOKEN(EQUAL);
"=="                    return TOKEN(DOUBLE_EQUAL);
"!="                    return TOKEN(NOT_EQUAL);
"<"                     return TOKEN(LT);
"<="                    return TOKEN(LET);
">"                     return TOKEN(GT);
">="                    return TOKEN(GET);
"("                     return TOKEN(OPEN_PARENT);
")"                     return TOKEN(CLOSE_PARENT);
"{"                     return TOKEN(OPEN_BRACE);
"}"                     return TOKEN(CLOSE_BRACE);
"."                     return TOKEN(DOT);
","                     return TOKEN(COMMA);
"+"                     return TOKEN(PLUS);
"-"                     return TOKEN(MINUS);
"*"                     return TOKEN(MULT);
"/"                     return TOKEN(DIV);
"&"                     return TOKEN(AND);
"|"                     return TOKEN(OR);
"!"                     return TOKEN(NOT);
"++"                    return TOKEN(INC);
"--"                    return TOKEN(DEC);
"*="                    return TOKEN(MULT_EQUAL);
"/="                    return TOKEN(DIV_EQUAL);
"+="                    return TOKEN(PLUS_SEQUAL);
"-="                    return TOKEN(MINUS_EQUAL);
"\p"                    return TOKEN(PRINT);
"\r"                    return TOKEN(RETURN);
"\b"                    return TOKEN(BREAK);
"while"                 return TOKEN(WHILE);
"if"                    return TOKEN(IF);
"else"                  return TOKEN(ELSE);
"elif"                  return TOKEN(ELIF);
"def"                   return TOKEN(DEF);
"for"                   return TOKEN(FOR);
""

%%