import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

class Lexer:

	reserved = {
	 'BIF' 		: 'IF',
	 'BELSE' 	: 'ELSE',
	 'BHILE' 	: 'WHILE',
	 'BOOP' 	: 'FOR',
	 'BETURN' 	: 'RETURN',
	 'BREAK' 	: 'BREAK',
	 'BAIN' 	: 'MAIN',
	 'BEND' 	: 'END',
	 'BEAD' 	: 'READ',
	 'BRINT' 	: 'PRINT',
	 'BTRING' 	: 'STRINGB', 
	 'BINT'		: 'INTB',
	 'BLOAT'	: 'FLOATB',
	 'BOOL'		: 'BOOLEANB',
	} 

	tokens = [
	'IDNAME', 'FLOAT', 'INT', 'STRING',

	#(+, -, *, /, %, ||, &&, !, <, <=, >, >=, ==, !=)
	'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'OR', 'AND', 'NOT',
    'LT', 'LEQ', 'GT', 'GEQ', 'EQ', 'NEQ',

    #ASSIGNMENT
    'ASSIGN',

    #Delimeters ( ) [ ] { } , ;
    'OPENAR', 'CLOSEAR', 'OPENBRACE', 'CLOSEBRACE', 'OPENCURLY', 'CLOSECURLY',
    'COMMA', 'SEMICOLON',
	] + list(reserved.values())

	def	t_IDNAME(t):
		r'[A-Za-z_][A-Za-z0-9_]*'
		t.var = Lexer.reserved.get(t.value, 'IDNAME')
		t.value = t.value.lower()
		return t

	# Integer literal
	def t_INT(t): 
		r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
		t.value = int(t.value)
		return t

	# Floating literal
	def t_FLOAT(t):
		r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
		t.value = float(t.value)
		return t

	# String literal
	def t_STRING(t):
		r'\"([^\\\n]|(\\.))*?\"'
		t.value = eval(t.value)
		t.value[1:-1]
		return t

	literals = '=', '+', '-', '*', '/', '%', '(', ')',

	#OPERATORS
	t_PLUS             = r'\+'
	t_MINUS            = r'-'
	t_MUL              = r'\*'
	t_DIV              = r'/'
	t_MOD              = r'%'
	t_OR               = r'\|\|'
	t_AND              = r'&&'
	t_NOT              = r'!'
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
	t_CLOSECURLY       = r'\}'
	t_COMMA            = r','
	t_SEMICOLON        = r';'

	# Identifiers

	def t_CPPCOMMENT(t):
	    r'//.*\n'
	    t.lexer.lineno += 1
	    return t

	def t_newline(t):
	    r'\n+'
	    t.lexer.lineno += t.value.count("\n")

	def t_error(t):
	    print("Illegal character '%s'" % t.value[0])
	    t.lexer.skip(1)

	def build(self, *kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
		return self.lexers

#import ply.lex as lex
#lex.lex()

#names{}
variableNames=[]
statementList=[]
var_names = {}

class Parser:

	tokens = Lexer.tokens

	precedence = (
		('right', 'ASSIGN'),
		('left', 'OR'),
		('left', 'AND'),
		('left', 'EQ', 'NEQ'),
		('left', 'LT', 'LEQ', 'GT', 'GEQ'),
		('left', 'PLUS', 'MINUS'),
		('left', 'MUL', 'DIV', 'MOD'),
		('left', 'OPENBRACE' , 'CLOSEBRACE', 'OPENAR' , 'CLOSEAR'),
	)

	def p_program_main(p):
		'program : programHead OPENCURLY var decl END CLOSECURLY'
		t[0] = 0

	def p_program_start(p):
		'programHead : MAIN OPENAR CLOSEAR'
		t[0] = 0

	def p_program_decl(p):
		'decl : var IDNAME nextdecl SEMICOLON decl'
		variableNames.append(t[2])
		names[t[2]]= ''

	def p_program_empty(p):
		'decl : empty'
		
	def p_program_decl_value(p):
		'decl : var IDNAME ASSIGN value nextdecl SEMICOLON decl'
		variableNames.append(t[2])
		names[t[2]] = t[4]

	def p_program_nextdecl(p):
		'nextdecl : COMMA IDNAME nextdecl'
		variableNames.append(t[2])
		names[t[2]]= ''
		
	def p_program_declassign(p):
		'nextdecl : COMMA IDNAME ASSIGN value nextdecl'
		variableNames.append(t[2])
		names[t[2]]=t[4]

	def p_program_emptydecl(p):
		'nextdecl : empty'

	def p_program_number(p):
		'''value : INT
				 | FLOAT'''
		t[0] = t[1]

	def p_program_var(p):
		'''var  : INTB
				| STRINGB
				| FLOATB
				| BOOLEANB'''
		p[0] = p[1]

	def p_statement_assign(p):
		'statement : IDNAME ASSIGN expression SEMICOLON statement'
		names[t[1]] = t[3]

	def p_statement_emptyState(p):
		'statement : empty'
		pass

	def p_statement_expression(p):
		'statement : expression'
		t[0] = t[1]

	def p_var_binop(p):
	    '''var : var PLUS var
	                  | var MINUS var
	                  | var MUL var
	                  | var DIV var
	                  | var MOD var'''
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

	def p_var_boolop(p):
	 	'''var : var GT var
	 				  | var LT var
	 				  | var GEQ var
	 				  | var LEQ var
	 				  | var EQ var
	 				  | var NEQ var'''
	 	if p[2] == 'GT':
	 		p[0] = p[1] > p[3]
	 	elif p[2] == 'LT':
	 		p[0] = p[1] < p[3]
	 	elif p[2] == 'GEQ':
	 		p[0] = p[1] >= p[3]
	 	elif p[2] == 'LEQ':
	 		p[0] = p[1] <= p[3]
	 	elif p[2] == 'EQ':
	 		p[0] = p[1] == p[3]
	 	elif p[2] == 'NEQ':
	 		p[0] = p[1] != p[3]

	def p_var_group(p):
		"var : '(' var ')'"
		p[0] = p[2]

	def p_error(p):
	    if p:
	        print("Syntax error at '%s'" % p.value)
	    else:
	        print("Syntax error at EOF")

	t_ignore = " \t"

	import ply.yacc as yacc
	yacc.yacc()

	while 1:
	    try:
	        s = raw_input('calc > ')
	    except EOFError:
	        break
	    if not s:
	        continue
	    yacc.parse(s)
