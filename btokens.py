tokens = [
	'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'BREAK', 'MAIN', 'END', 'READ', 'PRINT', 'STRING',
	'INT', 'FLOAT', 'BOOLEAN', 

	#(+, -, *, /, %, ||, &&, !, <, <=, >, >=, ==, !=)
	'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'OR', 'AND', 'NOT',
    'LT', 'LEQ', 'GT', 'GEQ', 'EQ', 'NEQ',

    #ASSIGNMENT
    'ASSIGN',

    #Delimeters ( ) [ ] { } , ;
    'OPENAR', 'CLOSEAR', 'OPENBRACE', 'CLOSEBRACE', 'OPENCURLY', 'CLOSECURLY',
    'COMMA', 'SEMICOLON',

]
#OPERATORS
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MODULO           = r'%'
t_OR               = r'\|\|'
t_AND              = r'\&\&'
t_NOT              = r'~'
t_LT               = r'<'
t_GT               = r'>'
t_LEQ              = r'<='
t_GEQ              = r'>='
t_EQ               = r'=='
t_NEQ              = r'!='

#ASSIGNMENT
t_ASSIGN           = r'='

#Delimeters
t_OPENAR           = r'\('
t_CLOSEAR          = r'\)'
t_OPENBRACE        = r'\['
t_CLOSEBRACE       = r'\]'
t_OPENCURLY        = r'\{'
t_CLOSEVURLY       = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'

# Identifiers
t_IDNAME = r'[A-Za-z_][A-Za-z0-9_]*'

# Integer literal
t_INTLIT = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FLTLIT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_STRLIT = r'\"([^\\\n]|(\\.))*?\"'

def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#
import ply.lex as lex
lex.lex()

#parsing rules
precedence = (
		('right', '='),
		('left', '||'),
		('left', '&&'),
		('left', '==', '!='),
		('left', '<', '<=', '>', '>='),
		('left', '+', '-'),
		('left', '*', '/', '%'),
		('left', '[]', '()'),

	)

#dictionary of names
names = {}

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
    	p[0] = p[1] % p[3]

import ply.yacc as yacc
yacc.yacc()