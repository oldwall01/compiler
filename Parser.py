from Tokenizer import *

# """"
# <program> ::= <func><func_list>				(1)
# <func_list> ::= <func><func_list>				(2)
# 			  ::= [] 				(3)
# <func> ::= <<id >> (<vars>) -> < <return_list> >
# 	{<var_decs><block>}					(4)
# 		::=  <<id>>(<vars>)->< <return_list> >          (5)
# <vars> ::= <var_dec><vars_tail>				(6)
# 		 ::= []						(7)
# <var_dec> ::= <type> << var_id >> <array_dec>			(8)
# <vars_tail> ::= ,<var_dec><vars_tail>				(9)
# 			  ::= []				(10)
# <var_decs> ::= <vars>;					(11)
# 			 ::= []					(12)
# <array_dec> ::= [<<int>>]					(13)
# 			  ::= []				(14)
# <return_list> ::= <type><return_tail>				(15)
# 				::= []				(16)
# <return_tail> ::= ,<type><return_tail>			(17)
# 				::= []				(18)
# <type> ::= int						(19)
# 		 ::= char					(20)
# 		 ::= bool					(21)
# <block> ::= <stmt><block>					(22)
# 		  ::= []					(23)
# """
######################################################################



# the keywords, single token, predefined the the program 
def keyword(S):
	if S in ['forward', 'if', 'while', 'write', 'read', 'int',
                         'char', 'bool', 'return', 'else']:
		return True
	else: return False

# the key symbol, single token, predefined the the program 
##def keySymbol(S):
##	if S in ['(', ')', ',', '<', '->', '>', ';', '[', ']', ':=',
##                         '{', '}', '>=', '<=', '!=', '+', '-', '*',
##                         '/', '%', '^', '!', '|', '&']:
##		return True
##	else: return False
	
# var_ID(S): return True when S is a string and could be a variable,
# in which the first char is a capital letter and any other is either letter, 
# digit or underline.
def var_ID(S):
	if (type(S) is str) and (not keyword(S)):	
		if not letter(S[0]): return False
		if S[0].islower(): return False
		for X in S:
			if not (letter(X) or digit(X) or X=='_'): return False
		return True
	else: return 
	
# id(S): return True when S is a string and could be a function ID,
# in which the first char is lower letter and any other is either letter, 
# digit or underline.
def id(S):
	if (type(S) is str) and (not keyword(S)):	
		if not letter(S[0]): return False
		if S[0].isupper(): return False
		for X in S:
			if not (letter(X) or digit(X) or X=='_'): return False
		return True
	else: return False
	
## define char type
def isChar(S):
	if (type(S) is str) and (len(S) == 3) and (S[0]=="\'") and (S[2] == "\'"):
		return True
	else: 
		return False
	

######################################################################
######################################################################
######################################################################

# <program> ::= <func><func_list>				(1)
# <func_list> ::= <func><func_list>			        (2)
# 			  ::= [] 				(3)
## Main parser function, input a list of tokens and return two elements
## If parser succeeds, the first element is the a nested list containg 
## the structure of program and the second is True; if fails, the first
## element returns None and second is False
## and the second
# Program is one or more functions
def program(P):
	(flag, P1) = func(P)
	if flag:
		P = P1
		(flag, P1) = func_list(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)

		
def func_list(P):
	if P == []:
		return (True, [])
	elif P[0] == 'forward' or id(P[0]):
			(flag, P1) = func(P)
			if flag:
				P = P1
				(flag, P1) = func_list(P)
				if flag:
					return (True, P1)
				else: 
					return (False, P1)
			else:
				return (False, P1)
	else: 
		print('Error: expecting begin with a function list or an empty list, but get ', P[0])
		return (False, P)
		
######################################################################

# <func> ::= <<id >> (<vars>) -> < <return_list> >
# 	{<var_decs><block>}					(4)
# 		::= forward<<id>>(<vars>)->< <return_list> >	(5)
#
# parsFunction(P) is True when either parseFunctionF(P) or
# parseFunctionN(P) is True
def func(P):
	if id(P[0]):
		P = P[1:]
		if P[0] == '(':
			P = P[1:]
			(flag, P1) = vars(P)
			if flag:
				P = P1
				if P[0] == ')':
					P = P[1:]
					if P[0] =='->':
						P = P[1:]
						if P[0] == '<':
							P = P[1:]
							(flag, P1) = return_list(P)
							if flag:
								P=P1
								if P[0] == '>':
									P = P[1:]
									if P[0] == '{':
										P = P[1:]
										(flag, P1) = var_decs(P)
										if flag:
											P=P1
											(flag, P1) = block(P)
											if flag:
												P=P1
												if P[0] == '}':
													return (True, P[1:])
												else:
													print('Error: expecting a \"}\", but get ', P[0])
													return (False, P)
											else:
												return (False, P1)
										else:
											return (False, P1)
									else:
										print('Error: expecting a \"{\", but get ', P[0])
										return (False, P)
								else:
									print('Error: expecting a \">\", but get ', P[0])
									return (False, P)
							else:
								return (False, P1)
						else:
							print('Error: expecting a \"<\", but get ', P[0])
							return (False, P)
					else:
						print('Error: expecting a \"->\", but get ', P[0])
						return (False, P)
				else:
					print('Error: expecting a \")\", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			print('Error: expecting a \"(\", but get ', P[0])
			return (False, P)
	elif P[0] == 'forward':
		P = P[1:]
		if id(P[0]):
			P = P[1:]
			if P[0] == '(':
				P = P[1:]
				(flag, P1) = vars(P)
				if flag:
					P = P1
					if P[0] == ')':
						P = P[1:]
						if P[0] =='->':
							P = P[1:]
							if P[0] == '<':
								P = P[1:]
								(flag, P1) = return_list(P)
								if flag:
									P=P1
									if P[0] == '>':
										return (True, P[1:])
									else:
										print('Error: expecting a \">\", but get ', P[0])
										return (False, P)
								else:
									return (False, P1)
							else:
								print('Error: expecting a \"<\", but get ', P[0])
								return (False, P)
						else:
							print('Error: expecting a \"->\", but get ', P[0])
							return (False, P)
					else:
						print('Error: expecting a \")\", but get ', P[0])
						return (False, P)
				else:
					return (False, P1)
			else:
				print('Error: expecting a \"(\", but get ', P[0])
				return (False, P)
		else:
			print('Error: expecting function ID, but get ', P[0])
			return (False, P)
	else:
		print('Error: expecting function ID or keyword \"forward\", but get ', P[0])
		return (False, P)
		

# <vars> ::= <var_dec><vars_tail>				(6)
# 		 ::= []						(7)

def vars(P):
	if P[0] == ')':
		return (True, P)
	elif P[0] == 'int' or P[0] == 'char' or P[0] == 'bool':
		(flag, P1) = var_dec(P)
		if flag:
			P = P1
			(flag, P1) = vars_tail(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting int, char, bool type or ")", but get ', P[0])
		return (False, P)
				
def var_dec(P):
	(flag, P1) = type1(P)
	if flag:
		P = P1
		if var_ID(P[0]):
			P = P[1:]
			(flag, P1) = array_dec(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			print('Error: expecting a variable ID, but get ', P[0])
			return (False, P)
	else:
		return (False, P1) 

def vars_tail(P):
	if P[0] == ',':
		P = P[1:]
		(flag, P1) = var_dec(P)
		if flag:
			P = P1
			(flag, P1) = vars_tail(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif P[0] == ')' or P[0] == ';':
		return (True, P)
	else:
		print('Error: expecting a ",", ")" or ";", but get ', P[0])
		return (False, P)

def var_decs(P):
	if P[0] == 'int' or P[0] == 'char' or P[0] == 'bool':
		(flag, P1) = var_dec(P)
		if flag:
			P = P1
			(flag, P1) = vars_tail(P)
			if flag:
				P = P1
				if P[0] == ';':
					return (True, P[1:])
				else:
					print('Error: expecting a ";", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif var_ID(P[0]) or id(P[0]) or P[0]=='if' or P[0]=='read' or P[0]=='return' or P[0]=='}' or P[0]=='write' or P[0]=='while':
		return (True, P)
	else:
		print('Error: expecting a variable ID, function ID, "if", "write", "read", "while", "}" or type char/int/bool, but get ', P[0])
		return (False, P)
		
def array_dec(P):
	if P[0] == ')' or P[0] == ';' or P[0] == ',':
		return (True, P)
	elif P[0] == '[':
		P = P[0]
		if type(P[0]) is int:
			P = P[0]
			if P[0] == ']':
				return (True, P[1:])
			else:
				print('Error: expecting a "]", but get ', P[0])
				return (False, P)
		else:
			print('Error: expecting a int, but get ', P[0])
			return (False, P)
	else:
		print('Error: expecting a ";", ")", "," or "[",  but get ', P[0])
		return (False, P)
		
def return_list(P):
	if P[0] == '>':
		return (True, P)
	elif P[0] == 'int' or P[0] == 'char' or P[0] == 'bool':
		(flag, P1) = type1(P)
		if flag:
			P = P1
			(flag, P1) = return_tail(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting int, char, bool type or ">", but get ', P[0])
		return (False, P)	

		
def return_tail(P):
	if P[0] == ',':
		P = P[1:]
		(flag, P1) = type1(P)
		if flag:
			P = P1
			(flag, P1) = return_tail(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif P[0] == '>':
		return (True, P)
	else:
		print('Error: expecting a "," or ">", but get ', P[0])
		return (False, P)	
		

def type1(P):
	if P[0] == 'int':
		return (True, P[1:])
	elif P[0] == 'char':
		return (True, P[1:])
	elif P[0] == 'bool':
		return (True, P[1:])
	else:
		print('Error: expecting "int"/"char"/"bool", but get ', P[0])
		return (False, P)
		



def block(P):
	if P[0] == '}':
		return (True, P)
	elif var_ID(P[0]) or P[0]=='if' or P[0]=='read' or P[0]=='write' or P[0]=='return' or P[0] =='while' or id(P[0]):
		(flag, P1) = stmt(P)
		if flag:
			P = P1
			(flag, P1) = block(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting begin with a statement or "}", but get ', P[0])
		return (False, P)

def stmt(P):
	if var_ID(P[0]):
		(flag, P1) = var_list(P)
		if flag:
			P = P1
			if P[0] == ':=':
				P = P[1:]
				(flag, P1) = arg_list(P)
				if flag:
					P = P1
					if P[0]==';':
						return (True, P[1:])
					else:
						print('Error: expecting ";", but get ', P[0])
						return (False, P)
				else:
					return (False, P1)
			else:
				print('Error: expecting ":=", but get ', P[0])
				return (False, P)
		else:
			return (False, P1)
	elif P[0] == 'if':
		P = P[1:]
		if P[0] == '(':
			P = P[1:]
			(flag, P1) = expr(P)
			if flag:
				P = P1
				if P[0] == ')':
					P = P[1:]
					if P[0] == '{':
						P = P[1:]
						(flag, P1) = block(P)
						if flag:
							P = P1
							if P[0] == '}':
								P = P[1:]
								(flag, P1) = else_tail(P)
								if flag:
									return (True, P1)
								else:
									return (False, P1)
							else:
								print('Error: expecting "}", but get ', P[0])
								return (False, P)
						else:
							return (False, P1)
					else:
						print('Error: expecting "{", but get ', P[0])
						return (False, P)
				else:
					print('Error: expecting ")", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			print('Error: expecting "(", but get ', P[0])
			return (False, P)
	elif P[0] == 'while':
		P = P[1:]
		if P[0] == '(':
			P = P[1:]
			(flag, P1) = expr(P)
			if flag:
				P = P1
				if P[0] == ')':
					P = P[1:]
					if P[0] == '{':
						P = P[1:]
						(flag, P1) = block(P)
						if flag:
							P = P1
							if P[0] == '}':
								return (True, P[1:])
							else:
								print('Error: expecting "}", but get ', P[0])
								return (False, P)
						else:
							return (False, P1)
					else:
						print('Error: expecting "{", but get ', P[0])
						return (False, P)
				else:
					print('Error: expecting ")", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			print('Error: expecting "(", but get ', P[0])
			return (False, P)
	elif P[0] == 'read':
		P = P[1:]
		if P[0] == '(':
			P = P[1:]
			(flag, P1) = var_list(P)
			if flag:
				P = P1
				if P[0] == ')':
					P = P[1:]
					if P[0] == ';':
						return (True, P[1:])
					else:
						print('Error: expecting ";", but get ', P[0])
						return (False, P)
				else:
					print('Error: expecting ")", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			print('Error: expecting "(", but get ', P[0])
			return (False, P)
	elif P[0] == 'return':
		P = P[1:]
		(flag, P1) = arg_list(P)
		if flag:
			P = P1
			if P[0] == ';':
				return (True, P[1:])
			else:
				print('Error: expecting ";", but get ', P[0])
				return (False, P)
		else:
			return (False, P1)
	elif id(P[0]):
		(flag, P1) = function_call(P)
		if flag:
			P = P1
			if P[0] == ';':
				return (True, P[1:])
			else:
				print('Error: expecting ";", but get ', P[0])
				return (False, P)
		else:
			return (False, P1)
	else:
		print('Error: expecting "if", "while", "write", "return", function ID or variable ID, but get ', P[0])
		return (False, P)

def var_list(P):
	(flag, P1) = var_ref(P)
	if flag:
		P = P1
		(flag, P1) = var_tail(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)
		
def var_tail(P):
	if P[0] == ':=' or P[0] == ')':
		return (True, P)
	elif P[0] == ',':
		P = P[1:]
		(flag, P1) = var_list(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting ",", ":=" or ")", but get ', P[0])
		return (False, P)
		
def var_ref(P):
	if var_ID(P[0]):
		P = P[1:]
		(flag, P1) = array_ref(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting variable ID,, but get ', P[0])
		return (False, P)

def array_ref(P):
	if P[0] in [",", ":=", ")", "*", "/", "+", "-", "<", ">", "=", "!=", "|", "&", ";", ">=", "<="]:
		return (True, P)
	elif P[0] == '[':
		P = P[1:]
		(flag, P1) = expr(P)
		if flag:
			P = P1
			if P[0] == ']':
				return (True, P[1:])
			else:
				print('Error: expecting "]",, but get ', P[0])
				return (False, P)
		else:
			return (False, P1)
	else:
		print('Error: expecting ",", ":=", ")", "*", "/", "+", "-", "<", ">", "=", "!=", "|", "&", ";", ">=", "<=" or "]",, but get ', P[0])
		return (False, P)
	
def else_tail(P):
	if var_ID(P[0]) or id(P[0]) or P[0]=='if' or P[0]=='read' or P[0]=='return' or P[0]=='}' or P[0]=='write' or P[0]=='while':
		return (True, P)
	elif P[0] == 'else':
		P = P[1:]
		if P[0] =='{':
			P = P[1:]
			(flag, P1) = block(P)
			if flag:
				P = P1
				if P[0] == '}':
					return (True, P[1:])
				else:
					print('Error: expecting "}",, but get ', P[0])
					return (False, P)
			else:
				(False, P1)
		else:
			print('Error: expecting "{",, but get ', P[0])
			return (False, P)
	else:
		print('Error: expecting a variable ID, function ID, "if", "write", "read", "while", "}" or "else", but get ', P[0])
		return (False, P)
		
def arg_list(P):
	(flag, P1) = arg(P)
	if flag:
		P = P1
		(flag, P1) = arg_tail(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)
		
def arg(P):
	if isChar(P[0]):
		return (True, P[1:])
	elif var_ID(P[0]) or id(P[0]) or (type(P[0]) is int) or (type(P[0]) is bool) or P[0] == '(':
		(flag, P1) = expr(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting a variable ID, function ID, int/bool type variable or "(", but get ', P[0])
		return (False, P)
			
		
def arg_tail(P):
	if P[0] == ';' or P[0] == ')':
		return (True, P)
	elif P[0] == ',':
		P = P[1:]
		(flag, P1) = arg_list(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting ",", ";" or ")", but get ', P[0])
		return (False, P)	
		
########################################################################
########################################################################

def expr(P):
	(flag, P1) = b_expr(P)
	if flag:
		P = P1
		(flag, P1) = expr_1(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)
		
def expr_1(P):
	if P[0] in [")", ",", ";", ]:
		return (True, P)
	elif P[0] == '|':
		P = P[1:]
		(flag, P1) = b_expr(P)
		if flag:
			P = P1
			(flag, P1) = expr_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif P[0] == '&':
		P = P[1:]
		(flag, P1) = b_expr(P)
		if flag:
			P = P1
			(flag, P1) = expr_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting "|", "&", ",", ";" or ")", but get ', P[0])
		return (False, P)	

		
def b_expr(P):
	(flag, P1) = n_expr(P)
	if flag:
		P = P1
		(flag, P1) = b_expr_1(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)


def b_expr_1(P):
	if P[0] in ["|", "&", ")", ",", ";"]:
		return (True, P)
	elif P[0] == '<':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	elif P[0] == '>':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	elif P[0] == '>=':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	elif P[0] == '>=':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	elif P[0] == '=':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	elif P[0] == '!=':
		P = P[1:]
		(flag, P1) = n_expr(P)
		if flag:
			return (True, P1)
		else:
			return (True, P1)
	else:
		print('Error: expecting "|", "&", ",", ";", "<", ">", "<=", ">=", "=", "!=" or ")", but get ', P[0])
		return (False, P)	



def n_expr(P):
	(flag, P1) = term(P)
	if flag:
		P = P1
		(flag, P1) = n_expr_1(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)


def n_expr_1(P):
	if P[0] in ["|", "&", ")", ",", ";", "<", ">", "<=", ">=", "!=", "="]:
		return (True, P)
	elif P[0] == '+':
		P = P[1:]
		(flag, P1) = term(P)
		if flag:
			P = P1
			(flag, P1) = n_expr_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif P[0] == '-':
		P = P[1:]
		(flag, P1) = term(P)
		if flag:
			P = P1
			(flag, P1) = n_expr_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting "+", "-", "|", "&", ",", ";", "<", ">", "<=", ">=", "=", "!=" or ")", but get ', P[0])
		return (False, P)
		
def term(P):
	(flag, P1) = factor(P)
	if flag:
		P = P1
		(flag, P1) = term_1(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		return (False, P1)	
		
def term_1(P):
	if P[0] in ["+", "-", "|", "&", ")", ",", ";", "<", ">", "<=", ">=", "!=", "="]:
		return (True, P)
	elif P[0] == '*':
		P = P[1:]
		(flag, P1) = factor(P)
		if flag:
			P = P1
			(flag, P1) = term_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	elif P[0] == '/':
		P = P[1:]
		(flag, P1) = factor(P)
		if flag:
			P = P1
			(flag, P1) = term_1(P)
			if flag:
				return (True, P1)
			else:
				return (False, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting "*", "/", "+", "-", "|", "&", ",", ";", "<", ">", "<=", ">=", "=", "!=" or ")", but get ', P[0])
		return (False, P)	

def factor(P):
	if var_ID(P[0]):
		(flag, P1) = var_ref(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	elif type(P[0]) is int:
		return (True, P[1:])
	elif type(P[0]) is bool:
		return (True, P[1:])
	elif P[0] == '!':
		P = P[1:]
		(flag, P1) = factor(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	elif P[0] == '(':
		P = P[1:]
		(flag, P1) = expr(P)
		if flag:
			P = P1
			if P[0] == ')':
					return (True, P[1:])
			else:
					return (False, P)
		else:
			return (False, P1)
	elif id(P[0]):
		(flag, P1) = function_call(P)
		if flag:
			return (True, P1)
		else:
			return (False, P1)
	else:
		print('Error: expecting  function ID, variable ID, int/bool variable type, "("or "!", but get ', P[0])
		return (False, P)	
		
########################################################################


def function_call(P):
	if id(P[0]):
		P = P[1:]
		if P[0] == '(':
			P = P[1:]
			(flag, P1) = call_list(P)
			if flag:
				P = P1
				if P[0] == ')':
					return (True, P[1:])
				else:
					print('Error: expecting ")", but get ', P[0])
					return (False, P)
			else:
				return (False, P1)
		else:
			print('Error: expecting "(", but get ', P[0])
			return (False, P)
	else:
		print('Error: expecting a variable ID, but get ', P[0])
		return (False, P)

def call_list(P):
	if P[0] == ')':
		return (True, P)
	elif var_ID(P[0]) or id(P[0]) or (type(P[0]) is int) or (type(P[0]) is bool) or P[0] == '(' or isChar(P[0]):
		(flag, P1) = arg_list(P)
		if flag:
			return(True, P1)
		else:
			(False, P1)
	else:
		print('Error: expecting a variable ID, function ID, int/bool/char type variable, ")", or "(", but get ', P[0])
		return (False, P)
