/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_PARSER_HPP_INCLUDED
# define YY_YY_PARSER_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    BREAK_LINE = 258,
    IDENTIFIER = 259,
    DOUBLE_EQUALINTEGER = 260,
    FLOAT = 261,
    EQUAL = 262,
    DOUBLE_EQUAL = 263,
    NOT_EQUAL = 264,
    LT = 265,
    LET = 266,
    GT = 267,
    GET = 268,
    OPEN_BRACE = 269,
    OPEN_PARENT = 270,
    CLOSE_BRACE = 271,
    CLOSE_PARENT = 272,
    DOT = 273,
    COMMA = 274,
    PLUS = 275,
    MINUS = 276,
    MULT = 277,
    DIV = 278,
    AND = 279,
    OR = 280,
    NOT = 281,
    INC = 282,
    DEC = 283,
    MULT_EQUAL = 284,
    DIV_EQUAL = 285,
    PLUS_EQUAL = 286,
    MINUS_EQUAL = 287,
    PRINT = 288,
    RETURN = 289,
    BREAK = 290,
    WHILE = 291,
    IF = 292,
    ELSE = 293,
    ELIF = 294,
    DEF = 295,
    FOR = 296
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_PARSER_HPP_INCLUDED  */
