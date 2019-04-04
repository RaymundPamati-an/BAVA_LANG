tokens = [
	'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'BREAK', 'MAIN', 'END', 'READ', 'PRINT', 'STRING',
	'INT', 'FLOAT', 'BOOLEAN', 'IDNAME', 'FLTLIT', 'INTLIT', 'STRLIT', 

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

literals = ['=', '+', '-', '*', '/', '%', '(', ')']

#Keywords
t_IF 			   = r'BIF'
t_ELSE			   = r'BELSE'
t_WHILE			   = r'BHILE'
t_FOR			   = r'BOOP' #LOOP
t_RETURN           = r'BETURN'
t_BREAK            = r'BREAK'
t_MAIN             = r'BAIN'
t_END              = r'BEND'
t_READ             = r'BEAD'
t_PRINT            = r'BRINT'

#Data Type
t_STRING           = r'BTRING'
t_INT              = r'BINT'
t_FLOAT            = r'BLOAT'
t_BOOLEAN          = r'BOOL'

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

#names{}
names = {}

def p_statement_assign(p):
    'statement : IDNAME "=" expression'
    names[p[1]] = p[3]
	
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

def p_expression_boolop(p):
 	'''expression : expression '>' expression
 				  | expression '<' expression
 				  | expression '>=' expression
 				  | expression '<=' expression
 				  | expression '==' expression
 				  | expression '!=' expression'''
 	if p[2] == '>':
 		p[0] = p[1] > p[3]
 	elif p[2] == '<':
 		p[0] = p[1] < p[3]
 	elif p[2] == '>=':
 		p[0] = p[1] >= p[3]
 	elif p[2] == '<=':
 		p[0] = p[1] <= p[3]
 	elif p[2] == '==':
 		p[0] = p[1] == p[3]
 	elif p[2] == '!=':
 		p[0] = p[1] != p[3]

def p_expression_group(p):
	"expression : '(' expression ')'"
	p[0] = p[2]

import ply.yacc as yacc
yacc.yacc()