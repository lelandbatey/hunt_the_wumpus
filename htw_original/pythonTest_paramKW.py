#====================================================================
# Russell Dean Swannack
# Washington State University, Tri-Cities
# CptS111: Introduction to Algorithmic Problem Solving
# November 15, 2012
# System: Python v3.2.3 IDLE (MS Windows OS)
#====================================================================
# Our TEST SCRIPT
def main():
	print('='*20)
	myTmpBool = awesome()
	print('='*20)
	myTmpBool = awesome(4, 5, 6, 'cat', 7)
	print('='*20)
	myTmpBool = awesome(myVolts=123.456, myText='Railroad')
	print('='*20)
	myTmpBool = awesome('box', 654.321, myThing = 'anaconda', myPI=3.14159, myName='Guido')	
	print('='*20)
	myStall=input('Press ENTER')
	return True
#====================================================================
# This functions accepts two types of parameters
# *arguments is a list of of unknown length of unamed paramters
# **keywords is a dictionary of named parameters and their values
def awesome(*arguments, **keywords):
	print('-=> awesome <=-', len(arguments), len(keywords))
	for arg in arguments:
		print(arg)
	print('-'*20)
	keys = sorted(keywords.keys())
	for kw in keys:
		print(kw, "is", keywords[kw])
	return True
#====================================================================
main()
