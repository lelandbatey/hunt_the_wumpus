#====================================================================
# Russell Dean Swannack
# Washington State University, Tri-Cities
# CptS111: Introduction to Algorithmic Problem Solving
# November 15, 2012
# System: Python v3.2.3 IDLE (MS Windows OS)
#====================================================================
# Basically we are using this as a Test/Demo script
def main():
	global gVarX # Declare this variable as GLOBAL for this function
	gVarX = 0 # Initialize it, mainly to prove a point
	print("\n1.main:", gVarX)

	myTmpBool = userInput() # Get another functions version
	print("\n2.main:", gVarX)
	
	myTmpBool = dispOutput() # Let another function print it out
	print("\n3.main:", gVarX)

	myTmpBool = resetGlobal() # Another function can set it
	print("\n4.main:", gVarX)

	myTmpBool = testLocal() # see what a LOCAL variable looks like
	print("\n5.main:", gVarX)
	
	myStall = input("\nPress ENTER") # wait to exit
	return True
#====================================================================	
# The USER is going to set the value of the global variable
def userInput():
	global gVarX
	gVarX = eval(input("\nuserInput: "))
	return True
#====================================================================
# We want to see what this functions thinks the global variable is
def dispOutput():
	global gVarX
	print("dispOutput:", gVarX)
	return True
#====================================================================
# This function is going to setting the global variable to a specific value
def resetGlobal():
	global gVarX
	gVarX = 123.456
	return True
#====================================================================
# All variables are automatically "LOCAL ONLY"
def testLocal():
	gVarX = eval(input("\nIN  testLocal: "))
	print("OUT testLocal:", gVarX)
	return True
#====================================================================
main() # run the test
