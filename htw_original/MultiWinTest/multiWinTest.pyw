#==================================================================
# Russell Dean Swannack
# Washington State University, Tri-Cities
# CptS111: Introduction to Algorithmic Problem Solving
# Homework Assignment #8: Chapter Four (Objects & Graphics)
# October 21, 2012
# System: Python v3.2.3 IDLE (MS Windows OS)
#==================================================================
# Required external library
from graphics import *
#==================================================================
def main():
	
	linuxFlag, theFilePath, theDelimOS = getPath()
	theFileName = ["btnOFF_rnd", "btnON_rnd"]
	theFileExt = ".gif"

	myWinA = GraphWin("Window One")
	myWinB = GraphWin("Window Two")
	myWinC = GraphWin("Window Three")
	myWinD = GraphWin("Window Four")

	btnAflag, btnBflag = 0, 0
	
	btnAimg = Image(Point(75,75), theFilePath+theFileName[btnAflag]+theFileExt)
	btnAimg.draw(myWinA)
	btnAimgW = btnAimg.getWidth()
	btnAimgH = btnAimg.getHeight()
	btnArad = abs(btnAimgW/2.0)
	if btnAimgH > btnAimgW: btnArad = abs(btnAimgH/2.0)
	buttonA = Circle(Point(75,75),btnArad)

	btnBimg = Image(Point(125,125), theFilePath+"btn"+str(btnBflag)+"_Rect"+theFileExt)
	btnBimg.draw(myWinB)
	btnBimgW = btnBimg.getWidth()/2.0
	btnBimgH = btnBimg.getHeight()/2.0
	buttonB = Rectangle(Point(125-btnBimgW,125-btnBimgH),Point(125+btnBimgW,125+btnBimgH))

	textC = Text(Point(100,100),"A")
	textC.setSize(20)
	textC.setStyle('bold')
	textC.draw(myWinC)
	
	textD = Text(Point(100,100),"B")
	textD.setSize(20)
	textD.setStyle('bold')
	textD.draw(myWinD)
	
	quitFlag = False
	while not quitFlag:

		try: umcA = myWinA.checkMouse()
		except: quitFlag = True
		
		if umcA != None:
			if gCircleIntersect(buttonA,umcA):
				btnAflag = abs(btnAflag-1)
				btnAimg = Image(Point(75,75), theFilePath+theFileName[btnAflag]+theFileExt)
				btnAimg.draw(myWinA)
				txtAC = "A: Button "+str(btnAflag)
			else:
				txtAC = "A: {0} {1}".format(umcA.getX(),umcA.getY())
			textC.setText(txtAC)
		
		try: umcB = myWinB.checkMouse()
		except: quitFlag = True
	
		if umcB != None:
			if gRectIntersect(buttonB,umcB):
				btnBflag += 1
				if btnBflag > 3: btnBflag = 0
				btnBimg = Image(Point(125,125), theFilePath+"btn"+str(btnBflag)+"_Rect"+theFileExt)
				btnBimg.draw(myWinB)
				txtBD = "B: Button "+str(btnBflag)
			else:
				txtBD = "B: {0} {1}".format(umcB.getX(),umcB.getY())
			textD.setText(txtBD)
			
		try: umcC = myWinC.checkMouse()
		except: quitFlag = True
		
		try: umcD = myWinD.checkMouse()
		except: quitFlag = True
		
	myWinA.close()
	myWinB.close()
	myWinC.close()
	myWinD.close()
	
	return True
#==================================================================
# Q01 # Purpose: Determine the length between two points (X,Y)
#       Passed In:  Two Point objects (graphics library)
#       Passed Out:  Distance between the two points
def gPtDist(myPt1, myPt2):
	theDist = ((myPt2.getX()-myPt1.getX())**2+(myPt2.getY()-myPt1.getY())**2)**0.5	
	return theDist
#==================================================================
# Q02 # Purpose: Determine if a point is within a circle
#       Passed In:  Circle object and a Point object (graphics library)
#       Passed Out:  Boolean Value: True = Test Point IS within the circle (includes boundary)
#                                   False = Test Point is NOT within the circle
def gCircleIntersect(myCircle,myPt):
	# Check to see if the point is within the circle and its boundary (perimeter)
	withinFlag = gPtDist(myCircle.getCenter(), myPt)<=myCircle.getRadius()
	return withinFlag
#===================================================================
# Purpose: To determine if a mouse click was inside of a given rectangle object or not
#-------------------------------------------------------------------
# Parameter (in): theRect (graphics Rectangle object handle) "Target" region
# Parameter (in): thePT (graphics Point object handle) user mouse click location
#-------------------------------------------------------------------
# Parameter (out): RectPt_Intersect (boolean) True = Point is within the Rectangle
#                                            False = Point is NOT within the Rectangle
#-------------------------------------------------------------------
def gRectIntersect(myRectangle, myPt):
	# Need to account for the possibility that the rectangle was constructed backwards
	rPt1X = min(myRectangle.getP1().getX(),myRectangle.getP2().getX())
	rPt2X = max(myRectangle.getP1().getX(),myRectangle.getP2().getX())
	rPt1Y = min(myRectangle.getP1().getY(),myRectangle.getP2().getY())
	rPt2Y = max(myRectangle.getP1().getY(),myRectangle.getP2().getY())
	tPtX, tPtY = myPt.getX(), myPt.getY() # Get Test Point Info
	# Check to see if the test point is within the rectangle bounds
	withinFlag = tPtX>=rPt1X and tPtX<=rPt2X and tPtY>=rPt1Y and tPtY<=rPt2Y
	return withinFlag
#====================================================================
# Purpose:
#     To provide the current working subdirectory where the application resides
# Inputs:
#     None.
# Outputs:
#     linuxOS  = The Operating System Flag (True=Linux/False=Windows)
#     filePath = The Default Subdirectory path to our application
#     delimOS = The Operating System specific subdirectory delimiter character
#-------------------------------------------------------------------
def getPath():
	""" OS Directory Pathname Retrieval """

	filePath = os.getcwd() # Get Current Working Subdirectory Path
	myOpSys = sys.platform # Get Operating System Platform identifier

	linuxOS = True # Assume we are using Linux
	delimOS = '/'  # The Linux subdirectory delimiter 
	if myOpSys.find('linux')<0: # Check to see if it is Linux or not
		linuxOS = False # Must not be; we assume it is MS Windows OS
		delimOS = '\\'  # The MS Windows OS subdirectory delimiter
	
	# Creates an "error" if this is not a ".py" file being executed
	# We are trying to acquire the local "file" name that is "running"
	try: tmpFL=len(__file__)
	except: tmpFL=-1 
	# Check to see what we are doing.
	if tmpFL<0: # We got the error; so we must be running in IDLE
		# Setup my specifically desired subdirectory location path
		filePath = 'C:\\Users\\Russell\\WSU CptS111 - Intro2Prog\\2012 Files - Fall\\'
		# If we are running under Linux; then I want a different subdirectory path
		if linuxOS: filePath = '/home/russell/Python_Projects'	
	filePath+=delimOS # finish up the subdirectory path
	return linuxOS, filePath, delimOS
#===================================================================
main()
