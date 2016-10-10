from Parser import *

######################################################################
## convert a syntax correct program, which is stored in a list of tokens, 
## to a list containing sublists, each of which carries meaningful units
## 1st element is function ID
## 2nd element is input parameters
## 3rd element is output 
## 4th element is variable decarations
## 5th element is a list containing all statements
def parseProgram(P):
	return parseFunction(P)
	
## helper function, return the corresponding index of the reverse parenthese, 
## includin ')', '>' and '}', in the list P
def nextParen(L, i):
	prenCount=0
	if L[i]=='(':
		prenCount+=1
		n=i+1
		while prenCount>0:
			if L[n]=='(': prenCount+=1
			if L[n]==')': prenCount-=1
			n+=1
		return n-1
	elif L[i]=='{':
		prenCount+=1
		n=i+1
		while prenCount>0:
			if L[n]=='{': prenCount+=1
			if L[n]=='}': prenCount-=1
			n+=1
		return n-1
	elif L[i]=='<':
		prenCount+=1
		n=i+1
		while prenCount>0:
			if L[n]=='<': prenCount+=1
			if L[n]=='>': prenCount-=1
			n+=1
		return n-1
	
	else: 
		print("Error: No parenthese found at current position!")
		return -1
## from back of a list to the from, find the index of '(' corresponding to current
## ')'
def reverseParen(L, i):
	prenCount=0
	if L[i]==')':
		prenCount+=1
		n=i-1
		while prenCount>0:
			if L[n]==')': prenCount+=1
			if L[n]=='(': prenCount-=1
			n-=1
		return n+1	
		
		
def nextSemicolon(L, i):
	n = i + 1
	while n < len(L):
		if L[n] == ';': 
			return n
		else:
			n += 1
	return None
		
def nextComma(L, i):
	n = i + 1
	while n < len(L):
		if L[n] == ',': 
			return n
		else:
			n += 1
	return None
		
	

def parseFunction(P):
	if P[0] == 'forward':
		print("Error: the function can't generate at current genQuad version!")
		return []
	else:
		funcID = P[0]
		IP = P[2:nextParen(P, 1)]
		OP = P[nextParen(P, 1) + 3: nextParen(P, nextParen(P, 1) + 2)]
		braceStart = nextParen(P, nextParen(P, 1) + 2) + 1
		if P[braceStart+1] in ['int', 'char', 'bool']:
			varDecsStart = braceStart + 1
			varDecs = P[varDecsStart: nextSemicolon(P, varDecsStart)] 
			blockStart = nextSemicolon(P, varDecsStart) + 1
		else:
			varDecsStart = braceStart + 1
			varDecs = []
			blockStart = braceStart + 1
		block = P[blockStart: len(P)-1]
		IPlist = parseIP(IP)
		OPlist = parseOP(OP)
		VarDecsList = parseVardecs(varDecs)
		blocklist = parseBlock(block)
		return [funcID] + [IPlist] + [OPlist] + [VarDecsList] + [blocklist]


def parseIP(P):
	if len(P) >= 2: 
		n = 0
		L = []
		while n < len(P):
			L = L + [[P[n], P[n+1]]]
			n += 3
		return L
	else:
		return []
		
def parseOP(P):
	OPlist= []
	i = 0
	while i < len(P):
		OPlist = OPlist + [P[i]]
		i += 2
	return OPlist

def  parseVardecs(P):
	if len(P) >= 2: 
		n = 0
		L = []
		while n < len(P):
			L = L + [[P[n], P[n+1]]]
			n += 3
		return L
	else:
		return []
	
def parseBlock(P):
	statements = []
	if P == []:
		return []
	else:
		i = 0
		while i < len(P):
			if P[i] == 'if':
				ifend = nextParen(P, nextParen(P, i+1) + 1)
				if ifend + 1 < len(P) and P[ifend + 1] == 'else':
					end = nextParen(P, ifend + 2)
				else:
					end = ifend
				statements = statements + [parseIfment(P[i : end + 1])]
				i = end + 1
			elif P[i] == 'while':
				end = nextParen(P, nextParen(P, i+1) + 1)
				statements = statements + [parseWhilement(P[i : end])]
				i = end + 1
			elif P[i]== 'read':
				end = nextSemicolon(P, i)
				statements = statements + [parseReadment(P[i : end])]
				i = end + 1
			elif P[i] == 'return':
				end = nextSemicolon(P, i)
				statements = statements + [parseReturnment(P[i : end])]
				i = end + 1
			elif id(P[i]):
				end = nextSemicolon(P, i)
				statements = statements + [parseFuncallment(P[i : end])]
				i = end + 1
			elif var_ID(P[i]):
				end = nextSemicolon(P, i)
				statements = statements + [parseAssignment(P[i : end])]
				i = end + 1
		return statements

		
def parseIfment(L):
	Ex = parseExpr(L[2: nextParen(L, 1)])
	blockend = nextParen(L, nextParen(L, 1) + 1)
	block1 = parseBlock(L[nextParen(L, 1) + 2 : blockend])
	if len(L) > blockend + 1 and L[blockend + 1] == 'else':
		block2 = parseBlock(L[blockend + 3 : len(L) -1])
		return ['if']+[Ex] + [block1] + ['else'] + [block2]
	else:
		return ['if'] + [Ex] + [block1]
	
	

def parseReadment(L):
	i = 2
	readment = ['readment']
	while i < len(L):
		readment = readment + [L[i]]
		i += 2
	return readment


def parseWhilement(L):
        
	print('the parser of while statement is still under construction!')
	

def	parseReturnment(L):
	i = 1
	returnment = ['returnment']
	while i < len(L):
		if isChar(L[i]):
			returnment = returnment + [L[i]]
			i += 2
		else:
			if nextComma(L, i) == None:
				returnment = returnment + [parseExpr(L[i : len(L)])]
				i = len(L)
			else:
				returnment = returnment + [parseExpr(L[i : nextComma(L, i)])]
				i = nextComma(L, i) + 1
	return returnment
	
	
def parseFuncallment(L):
	print('the parser of function call statement is still under construction!')
	
def parseAssignment(L):
	n = 0
	while L[n] != ':=':
		n += 1
	positionOfSign = n
	assignment = ['assignments']
	rightHandSide = []
	n += 1
	while n < len(L):
		if nextComma(L, n) == None:
			end = len(L)
			if len(L[n:end]) ==1 and isChar(L[n]):
				rightHandSide = rightHandSide + [L[n]]
			else:
				rightHandSide = rightHandSide + [parseExpr(L[n:end])]
			n = len(L)
		else:
			end = nextComma(L, n)
			if len(L[n:end]) ==1 and isChar(L[n]):
				rightHandSide = rightHandSide + [L[n]]
			else:
				rightHandSide = rightHandSide + [parseExpr(L[n:end])]
			n = end + 1
	i = 0
	while i < len(rightHandSide):
		assignment = assignment + [[':=', L[2*i], rightHandSide[i]]]
		i += 1       ## no array assignment is considered here
	return assignment
			
	
def parseExpr(L):
	i = len(L) - 1
	while i > 0:
		if L[i] == '|':
			return ['|', parseExpr(L[0 : i]), parseB_expr(L[i+1: len(L)])]
		elif L[i] == '&':
			return ['&', parseExpr(L[0 : i]), parseB_expr(L[i+1: len(L)])]
		elif L[i] == ')':
			i = reverseParen(L, i) -1
		else:
			i -= 1
	return parseB_expr(L)

def parseB_expr(L):
	i = len(L) - 1
	while i > 0:
		if L[i] == '<':
			return ['<', parseB_expr(L[0 : i]), parseN_expr(L[i+1: len(L)])]
		elif L[i] == '>':
			return ['>', parseB_expr(L[0 : i]), parseN_expr(L[i+1: len(L)])]
		elif L[i] == '=':
			return ['=', parseB_expr(L[0 : i]), parseN_expr(L[i+1: len(L)])]
		elif L[i] == '!=':
			return ['!=', parseB_expr(L[0 : i]), parseN_expr(L[i+1: len(L)])]
		elif L[i] == ')':
			i = reverseParen(L, i) -1
		else:
			i -= 1
	return parseN_expr(L)
	
def parseN_expr(L):
	i = len(L) - 1
	while i > 0:
		if L[i] == '+':
			return ['+', parseN_expr(L[0 : i]), parseTerm(L[i+1: len(L)])]
		elif L[i] == '-':
			return ['-', parseN_expr(L[0 : i]), parseTerm(L[i+1: len(L)])]
		elif L[i] == ')':
			i = reverseParen(L, i) -1
		else:
			i -= 1
	return parseTerm(L)
	
def parseTerm(L):
	i = len(L) - 1
	while i > 0:
		if L[i] == '*':
			return ['*', parseTerm(L[0 : i]), parseFactor(L[i+1: len(L)])]
		elif L[i] == '/':
			return ['/', parseTerm(L[0 : i]), parseFactor(L[i+1: len(L)])]
		elif L[i] == ')':
			i = reverseParen(L, i) -1
		else:
			i -= 1
	return parseFactor(L)
	
def parseFactor(L):
	if len(L) == 1:
		return L[0]
	elif L[0] == '(':
		return parseExpr(L[1:len(L) - 1])
	else:
		print('Error: parse factor, function call is not supported yet')
		

		
		
######################################################################
######################################################################
######################################################################
## generate symbol table from the program list
def symbolT(L):
	symbolT = [['index', 'Name', 'IO', 'Type', 'block']]
	symbolT = symbolT + [[20, L[0], 'proc', '', '']]
	funcIndex = symbolT[1][0]
	NofIP = 0 
	while NofIP < len(L[1]):
		prevIndex = len(symbolT) + 18
		symbolT = symbolT + [[prevIndex + 1, L[1][NofIP][1], 'IP', L[1][NofIP][0], funcIndex]]
		NofIP += 1
	NofOP = 0
	while NofOP < len(L[2]):
		prevIndex = len(symbolT) + 18
		symbolT = symbolT + [[prevIndex + 1, '#'+L[0]+'_'+str(NofOP), 'OP', L[2][NofOP], funcIndex]]
		NofOP += 1
	NofVardecs = 0
	while NofVardecs < len(L[3]):
		prevIndex = len(symbolT) + 18
		symbolT = symbolT + [[prevIndex + 1, L[3][NofVardecs][1], 'var', L[3][NofVardecs][0], funcIndex]]
		NofVardecs += 1
	constants = constantOf(L[4])
	n = 0
	while n < len(constants):
		prevIndex = len(symbolT) + 18
		if isChar(constants[n]):
			symbolT = symbolT + [[prevIndex + 1, constants[n], 'const', 'char', funcIndex]]
		else:
			symbolT = symbolT + [[prevIndex + 1, constants[n], 'const', 'int', funcIndex]]
		n += 1
	return symbolT

	
## retrieve all the constants (including char and int) from the statement 
## list, including the sublist.
def constantOf(L):
	C = []
	i = 0
	while i < len(L):
		if isChar(L[i]) or (type(L[i]) is int):
			if L[i] not in C:
				C = C + [L[i]]
			else:
				C = C + []
		elif type(L[i]) is str:
			C = C + []
		else:
			for X in constantOf(L[i]):
				if X in C:
					C = C + []
				else:
					C = C + [X]
		i += 1
	return C
	

	
######################################################################
######################################################################
######################################################################

## look up the index address of a symbol in the symbol table
## T is the table
def AddressOf(T, Name, Block):
	for X in T:
		if X[1] == Name and X[4] == Block:
			return X[0]
	return None

	
def typeOf(T, Name, Block):
	for X in T:
		if X[1] == Name and X[4] == Block:
			return X[3]
	return None	
	
def currentFunc(T, entryIndex):
	for X in T:
		if X[0] == entryIndex:
			return X[1]
	return None
	


def quadsOfBlock(L, T, entryIndex, offset):
	quads = []
	i = 0
	while i < len(L):
		if L[i][0] == 'assignments':
			quads = quads + quadsOfAssignments(L[i], T, entryIndex)
		elif L[i][0] == 'if':
			quads = quads + quadsOfIfment(L[i], T, entryIndex, offset + len(quads))
		elif L[i][0] == 'readment':
			quads = quads + quadsOfReadment(L[i], T, entryIndex)
		elif L[i][0] == 'returnment':
			quads = quads + quadsOfReturnment(L[i], T, entryIndex)
		i += 1
	return quads
	

def quadsOfAssignments(L, T, entryIndex):
	quads = []
	i = 1
	while i < len(L):
		if isChar(L[i][2]):
			quads = quads + [['assign', AddressOf(T, L[i][2], entryIndex), '_', AddressOf(T, L[i][1], entryIndex)]]
		else:
			(exprQuads, tempReg) = quadsOfExpr(L[i][2], T, entryIndex, 100)
			quads = quads + exprQuads
			quads = quads + [['assign', tempReg, '_', AddressOf(T, L[i][1],  entryIndex)]]
		i += 1
	return quads
		


def quadsOfIfment(L, T, entryIndex, offset):
	quads = []
	(exprQuads, tempReg) = quadsOfExpr(L[1], T, entryIndex, 100)
	quads = quads + exprQuads
	ifblockQuads = quadsOfBlock(L[2], T, entryIndex, len(quads) + offset + 1)
	if len(L) > 3  and L[3] == 'else':
		quads = quads + [['jumpfalse', tempReg, '_', len(quads) + len(ifblockQuads) + offset + 3]]
		quads = quads + ifblockQuads
		elseblockQuads = quadsOfBlock(L[4], T, entryIndex, len(quads) + offset + 1)
		quads = quads + [['jump', '_', '_', len(quads) + len(elseblockQuads) + offset + 2]]
		quads = quads + elseblockQuads
	else:
		quads = quads + [['jumpfalse', tempReg, '_', len(quads) + len(ifblockQuads) + offset + 2]]
		quads = quads + ifblockQuads
	return quads	



def quadsOfReadment(L, T, entryIndex):
	quads = []
	i = 1
	while i < len(L):
		if typeOf(T, L[i], entryIndex) == 'char':
			quads = quads + [['inchar', '_', '_', AddressOf(T, L[i], entryIndex)]]
		elif typeOf(T, L[i], entryIndex) == 'int':
			quads = quads + [['inint', '_', '_', AddressOf(T, L[i], entryIndex)]]
		i += 1
	return quads
	
	
def quadsOfReturnment(L, T, entryIndex):
	quads = []
	i = 1
	while i < len(L):
		if typeOf(T, L[i], entryIndex) == 'char':
			quads = quads + [['assign',  AddressOf(T, L[i], entryIndex), '_', AddressOf(T, '#'+currentFunc(T, entryIndex)+'_'+str(i-1), entryIndex)]]
		else:
			(exprQuads, tempReg) = quadsOfExpr(L[i], T, entryIndex, 100)
			quads = quads + exprQuads
			quads = quads + [['assign', tempReg, '_', AddressOf(T, '#'+currentFunc(T, entryIndex)+'_'+str(i-1), entryIndex)]]
		i += 1
	return quads
	
	
def quadsOfExpr(L, T, entryIndex, regTaken):
	quads = []
	if var_ID(L):
		tempReg = AddressOf(T, L, entryIndex)
		return ([], tempReg)
	elif (type(L) is int) or (type(L) is bool):
		tempReg = AddressOf(T, L, entryIndex)
		return ([], tempReg)
	elif L[0] == '|':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['or', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '&':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['and', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))	
	elif L[0] == '<':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['lt', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))			
	elif L[0] == '>':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['gt', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '=':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['eq', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '!=':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['neq', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '*':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['mult', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '/':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['div', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '+':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['add', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))
	elif L[0] == '-':
		(exprQuads1, OP1) = quadsOfExpr(L[1], T, entryIndex, regTaken)
		quads = quads + exprQuads1
		if type(OP1) is str and OP1[0] == 'T':
			regTaken = int(OP1[1:4])
		(exprQuads2, OP2) = quadsOfExpr(L[2], T, entryIndex, regTaken)
		quads = quads + exprQuads2
		if type(OP2) is str and OP2[0] == 'T':
			regTaken = int(OP2[1:4])
		quads = quads + [['sub', OP1, OP2, 'T' + str(regTaken+1)]]
		return (quads, 'T'+ str(regTaken+1))

###########################################################
###########################################################
###########################################################
	
## generate quads
def genQuad(P):
	(tok, flag) = tokenize(P)
	if flag:
		if program(tok)[0]:
			L = parseProgram(tok)
		else:
			print('Error: syntax fails')
			return None
	ST = symbolT(L)
	quads = []
	entryIndex = AddressOf(ST, L[0], '')
	quads = quads + [['procentry', entryIndex, '_' , '_']]
	quads = quads + quadsOfBlock(L[4], ST, entryIndex, len(quads))
	quads = quads + [['procexit', ST[1][0], '_' , '_']]
	print('The symbol table is as follows:')
	i = 0
	while i < len(ST):
		print(ST[i])
		i += 1
	print('\n','The quads generated are as follows:')
	i = 0
	while i < len(quads):
		print(i+1, '\t', quads[i])
		i += 1

	

		
		
		
