


##"""
##If S is a list of characters, munch(S) is the result of greedily trying 
##to form the longest possible token from the start of S, one character 
##at a time. munch(S) destroys its argument.
##Helper functions are canPush , newState, charsToTok, validToken
##"""
######################################################################
def letter(C):
	if ord(C)>=65 and ord(C) <=90: return True
	elif ord(C) >=97 and ord(C) <= 122: return True
	else: return False

def digit(C):
	if ord(C)>=48 and ord(C) <=57: return True
	else: False
	
def alSymb(C):
	if ord(C) in [33, 42, 43, 47, 60, 62]: return True
	else: return False

def colonS(C):
	if ord(C) == 58: return True
	else: return False

def minusS(C):
	if ord(C) == 45: return True
	else: return False

def whitespace(C):
	if ord(C) in [9,10,11,12,13,32]: return True
	else: return False
	
	
def special(C):
	if letter(C) or digit(C) or whitespace(C) :
		return False
	elif alSymb(C) or colonS(C) or minusS(C) or C=='\'' or C=='\"':
		return False
	else: return True
	
######################################################################

## newState(state, C), retruns the new 'state' after the token list with 
## 		previous 'state' after adding a new char C

def newState(state, C):
	if state == 'empty':
		if letter(C):	return 'atom'
		elif digit(C):	return 'number'
		elif alSymb(C): return 'alSymbol'
		elif colonS(C): return 'colon'
		elif minusS(C):	return 'minusSign'
		elif special(C):return 'special'
		elif C=='\'': return 'singlequotation'
		elif C=='\"': return 'doublequotation'
	elif state == 'atom' and (letter(C) or digit(C) or C=='_'):
		return 'atom'
	elif state == 'number' and digit(C): return 'number'
	elif state == 'number' and C=='.': return 'fnumber'
	elif state == 'fnumber' and digit(C): return 'floatNumber'
	elif state == 'floatNumber' and digit(C): return 'floatNumber'
	elif state == 'alSymbol' and C=='=': return 'doublealSymbol'
	elif state == 'colon' and C=='=': return 'assignSymbol'
	elif state == 'minusSign' and C=='=': return 'doublealSymbol'
	elif state == 'minusSign' and C=='>': return 'funcSign'
	elif state == 'singlequotation' and C != '\'': return 'charInProgress'
	elif state == 'charInProgress' and C == '\'': return 'char'
	elif state == 'doublequotation' and C != '\"': return 'stringInProgress'
	elif state == 'stringInProgress' and C == '\"': return 'string'
	

## canPush(C, state) means the token char list can list can accept
## 		C into the into list and make the state a valid token state.

def canPush(C, state):
	if state == 'empty' or state == 'stringInProgress' or state == 'doublequotation': return True
	elif state == 'atom' and (letter(C) or digit(C) or C=='_'):
		return True
	elif state == 'number' and (digit(C) or C=='.'): return True
	elif state == 'fnumber' and digit(C): return True
	elif state == 'floatNumber' and digit(C): return True
	elif state == 'alSymbol' and C=='=': return True
	elif state == 'colon' and C=='=': return True
	elif state == 'minusSign' and C=='>': return True
	elif state == 'singlequotation' and C != '\'': return True
	elif state == 'charInProgress' and C == '\'': return True
	else: return False

######################################################################

## charsToTok(Charlist): Charlist is a list of chars and charsToTok 
## convert is to a string 
def charsToTok(Charlist, state):
	a = ''.join(Charlist)
	if state=='number': return int(a)
	elif state in ['fnumber', 'floatNumber']: return float(a)
	else: return a

## when state is one either 'atom', 'number', 'alSymb', 'special',
## 'colon'  or 'assignSymbol', it's a valid token	
def validToken(state):
	if state in ['atom', 'number', 'alSymbol', 'colon', 'minusSign',
                     'special', 'fnumber', 'floatNumber',
                     'doublealSymbol', 'assignSymbol', 'funcSign', 'char', 'string']:
		return True
	else: return False

##"""
##munch(S):
##	chars = [],
##	state = 'empty',
##	while S != [] and canPush(head(S),state):
##		remove the first character of S and add it to the \
##		end of chars,
##		state := newState(state,c)
##	if validToken(state): return (charsToTok(chars), True))
##	else: return(None,False)
##"""

def munch(S):
	chars = []
	state = 'empty'
	while S != '' and canPush(S[0], state):
		chars = chars + [S[0]]
		state = newState(state, S[0])
		S = S[1:]
	if validToken(state): 
		return (charsToTok(chars, state), True, S)
	else: return (None, False, S)
	
	
######################################################################
##"""
##tokens(S):
##	tokens = []
##	remove all initial white space from S,
##	while S is not empty
##		remove all initial white space from S,
##		(token,Flag) := munch(S)
##		if Flag:
##			tokens := tokens + [token]
##		else
##			return (None,False)
##	return (tokens,True)
##"""

def tokenize(S):
	tokens = []
	while S!='' and whitespace(S[0]):
		S = S[1:]
	while S != '':
		while S!='' and whitespace(S[0]):
			S = S[1:]
		(token, Flag, S1) = munch(S)
		if Flag:
			tokens = tokens + [token]
			S = S1
		else:
			break

	if tokens != []: return (tokens, True)
	else: return(None, False)
	


######################################################################
######################################################################
