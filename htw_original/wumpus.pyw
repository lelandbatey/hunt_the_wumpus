'''
Leland Batey
WSU Tri-Cities
Cpts 111
Hunt the Wumpus - Final Assignment
Assignment Due December 02, 2012 (by Midnight)
Began work 26th October, 

Create the classic "Hunt the Wumpus" game on a square grid.

Development Environment:
    OS - Windows 8
    Software Version - Python 3.2
Intended to be run on the Windows Operating System

'''
from graphics import *
from random import *
from pprint import pprint
import time

# ====== Get Difficulty ======
# Presents the user with a window for selecting the difficulty (easy, medium or hard)
#   Represented as a single integer:
#   0 - Easy
#   1 - Medium
#   2 - Hard
#
#   This data is storred in the global variable "gameDiff"
def getDiff():
    global gameDiff
    diff = GraphWin("Choose the difficulty!", 400,100)
    doneFlag = False
    easyBtn = Rectangle(Point(66,36),Point(134,64))
    mediumBtn = Rectangle(Point(166,36),Point(234,64))
    hardBtn = Rectangle(Point(266,36),Point(334,64))
    bttnPnts = [[100,50],[200,50],[300,50]]
    bttnNames = ["easybutton.gif",'mediumbutton.gif','hardbutton.gif']
    for point in bttnPnts:
        Image(Point(point[0],point[1]),bttnNames[bttnPnts.index(point)]).draw(diff)

    # Quitgame is a variable that catches whether the user clicked the red x button on the "choose difficulty" window. The "main()" function uses it to define "doneFlag so that it will end the game at that."
    quitGame = False

    while not doneFlag:
        try:
            myClick = diff.getMouse()
        except GraphicsError:
            quitGame = True
            doneFlag = True
            gameDiff = 0
        if not doneFlag:
            if gRectIntersect(easyBtn,myClick):
                print("Easy")
                gameDiff = 0
                doneFlag = True 
            elif gRectIntersect(mediumBtn,myClick):
                print("Medium")
                gameDiff = 1
                doneFlag = True
            if gRectIntersect(hardBtn,myClick):
                print("Hard")
                gameDiff = 2
                doneFlag = True
    diff.close()
    return quitGame
    
# ====== Check if Click is Inside Rectangle ======
# Requires that a Rectangle and Point object be passed
# Checks to see if the point (presumed to be the user's mouse click) falls within the area of the given Rectangle object
# Written by Russel Swannack
# Used with permission.
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

# ====== Building The Game Data Skeleton ======
# Difficulty   : Integer between 0 and 2
# topLeftPoint : List with two entries, the X and Y (in that order) pixel points of the top left point
# numPixels    : Integer of number of pixels wide that the board must be (defaults to 400)
def buildGameGrid(difficulty,topLeftPoint=[2,2],numPixels=400):
##'''This module will build the data structure in a three dimensional array:
##First level: The row of data
##Second level: The "game square" in the row (or the colum number)
##Third level: Contains all the actual data, in the following order:
##    [0] An array with two values: the X and Y coordinates of the top left game square (in that order).
##    [1] An array with two values: the X and Y coordinates of the lower right game square (in that order).
##    [2] An array with two values: the X and Y coordinates of the pixel at the center of the game square (in that order).
##    [3] A boolean value for whether there is a wumpus in this game square.
##    [4] A boolean value for whether there is treasure in this game square.
##    [5] A boolean value for whether there is a pit in this game square.
##    [6] A boolean value for whether the player has visited that game square.
##    [7] A Text object containing what is "sensed" in this game square, formated as follows:
##        "S B G" - "stench," "breaze," and "Glitter" in that order.
##        If one of these is not present it will be replaced with a "-" character to signify no sense of that kind.
##
##This loop will initially only fill the first three values (upper left, lower right, and center point coordinates).
##All other values will be set to default values (False for booleans, "-" for strings). These other values will be
##calculated in other modules.'''
    global gameDiff # Accesses the global variable for the level of difficulty
    
    # Based on the difficulty of this game instance, initNumSquares is set to the appropriate value
    # initNumSquares represents the number of squares in each row and column of the game board. Because the game board is a square, the number of rows and columns is the same, thus there is only one value for both.
    if gameDiff == 0:
        initNumSquares = 8
    elif gameDiff == 1:
        initNumSquares = 9
    elif gameDiff == 2:
        initNumSquares = 10

    # Alright, this is a super hack to fix stuff some problems that I'm having, but I don't care
    #initNumSquares += 1
    
    divFactor = numPixels//initNumSquares

    priorPoint = topLeftPoint
    gridList,tmpList,lowRightTmp,centerPntTmp = [],[],[],[] # gridList will be the final array

    for rowCnt in range(initNumSquares):
        gridList.append([])
        for columnCnt in range(initNumSquares):
            lowRightTmp = [priorPoint[0]+divFactor,priorPoint[1]+divFactor] # Calculates lower right point of the game square.
            centerPntTmp = [int(priorPoint[0]+divFactor/2),int(priorPoint[1]+divFactor/2)] # calculates the center point

            # vvv - That command appends everything to the list, including default values for what the square contains and what you sense when entering this square.
            #tmpList.append(priorPoint,lowRightTmp,centerPntTmp,False,False,False,False,"- - -")
            for i in [priorPoint,lowRightTmp,centerPntTmp,False,False,False,False,Text(Point(centerPntTmp[0],centerPntTmp[1]-(15/10*initNumSquares)),"- - -")]:
                tmpList.append(i)
            gridList[rowCnt].append(tmpList)

            priorPoint = [priorPoint[0]+divFactor,priorPoint[1]] # Iterates prior point to the next point
            tmpList=[]

        priorPoint = [topLeftPoint[0],(rowCnt+1)*divFactor+2] # Resets priorPoint, but increments the Y to the beginning of the next row

    # Sets up the location of game elements like treasure, wumpus, etc
    gridList,deadWumpusList = placeGameElements(gridList,gameDiff)
    
    return gridList,deadWumpusList


# ====== Create List of Random Points ======
# Requires minimum and maximum values for the radomly generated numbers, as well as the total amount of random integers to be generated.       
# This function was written by Russell Swannack for Cpts 111 HW 09 - Q 04
# Modified and used with permission
def xyListCreate(iMinNum,iMaxNum,iTotNum):
    xyList = [] # Initialize the List
    # Keep looping until we have the number of required XY pairs
    while len(xyList) < iTotNum: 
        # Create a random XY Pair
        tmpXY = [randint(iMinNum,iMaxNum),randint(iMinNum,iMaxNum)]
        # If it is not already in the list, append it to the list
        if not tmpXY in xyList: xyList.append(tmpXY)
    return xyList

# ====== Sets Random Positions of Game Objects ======
# Based on the difficulty, this places game objects (wumpus, pit, gold) on the virtual game board (vBoard) by setting the appropriate flags in the selected squares to True
# Requires that the game board and difficulty be passes (if the difficuly is not passed, it defualts to a difficulty of 1)
def placeGameElements(vBoard,difficulty=1):

    # A list which shall containg 2 lists:
    #   Each sub-list will contain the virtual X and Y coordinates of a wumpus on the game board, as well as a boolean value which keeps track of whether that wumpus is alive or dead (False = Alive, True = Dead)
    deadWumpusList = []


    # Based on the provided difficulty, the game sets the number of pits, treasures, and wumpii to be placed on the game board.
    if difficulty == 0:
        pits = randint(10,15)
        treasure = randint(10,15)
        wumpus = 1
        numSquares = 7
    elif difficulty == 1:
        pits = randint(15,20)
        treasure = randint(10,15)
        wumpus=1
        numSquares = 8
    elif difficulty == 2:
        pits = randint(15,20)
        treasure = randint(15,20)
        wumpus = 2
        numSquares = 9 # Set one lower than normal to account for list beginning at 0
    else: print("difficulty error")

    # Each <object>Points variable is a list containing an appropriate number of sub-lists of the virtual coordinates where a game object will be placed on the vitual game board.
    pitPoints = xyListCreate(0,numSquares,pits)
    treasurePoints = xyListCreate(0,numSquares,treasure)
    wumpusPoints = xyListCreate(0,numSquares,wumpus)

    # Iterates through each list of points of game objects, then changes the cooresponding value in the given game square
    for coords in pitPoints:
        vBoard[coords[0]][coords[1]][5] = True
    for coords in treasurePoints:
        vBoard[coords[0]][coords[1]][4] = True
    for coords in wumpusPoints:
        vBoard[coords[0]][coords[1]][3] = True
        deadWumpusList.append([coords[1],coords[0],False])

    vBoard = setSenses(vBoard)
    
    return vBoard, deadWumpusList

# ====== Sets the Sense Data for Each Game Square ======
# Requires the virtual board data (vBoard)
def setSenses(vBoard):
##"""
##Looks at the board, and checks if an adjacent square has a game object in it (wumpus, treasure, or pit).
##If there is a game object next to it, then it set's it's own "sense" attribute accordingly.
##"""

    # Each of these numbers is the position in the gameSquare objects data list.
    #   For example, the item in position 5 in a gameSquares attribute list will always contain the boolean value for whether that gameSquare has a pit in it.
    pit=5
    treasure=4
    wump=3
    
    for rowCnt in range(len(vBoard)):
        # Resets sense data for this loop
        stench = False
        glitter = False
        breeze = False
        for colCnt in range(len(vBoard)):
            # Resets sense data for this loop
            stench = False
            glitter = False
            breeze = False
            senseString = ""

            # Checks all adjacent rows for game objects
            # try:
            #     if vBoard[abs(rowCnt-1)][colCnt][pit] or vBoard[rowCnt][abs(colCnt-1)][pit] or vBoard[abs(rowCnt+1)][colCnt][pit] or vBoard[rowCnt][abs(colCnt+1)][pit]:
            #         breeze = True
            # except: pass
            # try:
            #     if vBoard[abs(rowCnt-1)][colCnt][treasure] or vBoard[rowCnt][abs(colCnt-1)][treasure] or vBoard[abs(rowCnt+1)][colCnt][treasure] or vBoard[rowCnt][abs(colCnt+1)][treasure]:
            #         glitter = True
            # except: pass
            # try:
            #     if vBoard[abs(rowCnt-1)][colCnt][wump] or vBoard[rowCnt][abs(colCnt-1)][wump] or vBoard[abs(rowCnt+1)][colCnt][wump] or vBoard[rowCnt][abs(colCnt+1)][wump]:
            #         stench = True
            # except: pass

            # For this square, checks if an adjacent square has a pit, gold, or wumpus in it, then sets the appropriate boolean value
            breeze =  getAdjacent([colCnt,rowCnt],vBoard,pit)
            glitter = getAdjacent([colCnt,rowCnt],vBoard,treasure)
            stench = getAdjacent([colCnt,rowCnt],vBoard,wump)


            # Based on the sense evaluation above, builds the senseString
            if stench: senseString += "S "
            else: senseString += "- "
            
            if breeze: senseString += "B "
            else: senseString += "- "

            if glitter: senseString += "G"
            else: senseString += "-"

            # Sets the correct Text object for this square, as well as it's text color, size and typeface
            vBoard[rowCnt][colCnt][7].setText(senseString)
            vBoard[rowCnt][colCnt][7].setFace('courier')
            vBoard[rowCnt][colCnt][7].setSize(6)
            vBoard[rowCnt][colCnt][7].setTextColor('white')

    return vBoard
# ====== Generic Function for Finding the Objects in Adjacent Squares =======
# vCoords : Virtual coordinates of the game square
# vBoard  : Virtual game board data
# obj     : Integer which is reference to game object flag in game square data in vBoard. 3, 4, and 5 are valid values.
def getAdjacent(vCoords,vBoard,obj):
## This is a function to evaluate adjacent senses.
## vCoords is a list with the X and Y virtual points of the location of a square on the gameBoard
## This was written to more elegantly handle the problem of finding the correct objects around a square.
    sense = False
    try:
        if vBoard[abs(vCoords[1]-1)][vCoords[0]][obj]:
            sense = True
    except:
        print("rowCnt:",vCoords[1],"colCnt:",vCoords[0],"Checking: Row - 1")
    
    try:
        if vBoard[vCoords[1]][abs(vCoords[0]-1)][obj]:
            sense = True
    except:
        print("rowCnt:",vCoords[1],"colCnt:",vCoords[0],"Checking: Col - 1")
    
    try:
        if vBoard[vCoords[1]+1][vCoords[0]][obj]:
            sense = True
    except:
        print("rowCnt:",vCoords[1],"colCnt:",vCoords[0],"Checking: Row + 1")
    
    try:
        if vBoard[vCoords[1]][vCoords[0]+1][obj]:
            sense = True
    except:
        print("rowCnt:",vCoords[1],"colCnt:",vCoords[0],"Checking: Col + 1")

    return sense


# ====== NON-IMPLEMENTED FUNCTION ======
# This function is not actually used anywhere in the program. However, it was used during development to make the placement of buttons and rectangles easier.         
def btnSize():
    # I wrote this so I won't have to do so much tedious math to get the points for rectangles for buttons.
    btnW = eval(input("Button width: "))
    btnH = eval(input("Button height: "))
    btnCentX,btnCentY = eval(input("Button center point X and Y, command separated: "))
    print("Top left point : ",btnCentX-(btnW/2),btnCentY-(btnH/2))
    print("Lower right point: ",btnCentX+btnW/2,btnCentY+btnH/2)
    print("Rectangle(Point("+str(int(btnCentX-(btnW/2)))+","+str(int(btnCentY-(btnH/2)))+"),Point("+str(int(btnCentX+btnW/2))+","+str(int(btnCentY+btnH/2))+"))")

# ====== Initailizing the Game Character ======
# vBoard : Virtual game board data
def initGameChar(vBoard,gameChar=[]):
##"""
##Initializes the game character. It checks every square on the board from left to right, top to bottom,
##and if there is not a game object (wumpus, treasure, pit), then it places the game character there.
##However, it will still continue to search for empty squares, and every time it finds one, it will
##place the character in the square, until it runs out of squares. For this reason, this function favors
##placing the character in the lower right corner of the board.
##"""
# Game Character Data Structure:
#     [0] - X position on the virtual game grid
#     [1] - Y position on the virtual game grid
#     [2] - Image object on the center pixel coordinates of the real game square, with the characters sprite

    # Accessing the main window and the game difficulty
    global win
    global gameDiff


    # This loop iterates through the game board, checking to see if the current space is empty. If it is, it sets the character's position to that square. However, it continues the process, repeatedly setting the players position to every blank sqare. Because of this, the player will have  a tendency to be placed in teh lower right corner of the board.
    print(len(vBoard))
    for rowCnt in vBoard:
        for colCnt in rowCnt:
            if not colCnt[3] and not colCnt[4] and not colCnt[5]:
                gameChar = [rowCnt.index(colCnt),vBoard.index(rowCnt)]
    print(gameChar)

    # The long array reference refers to the virtual square inhabited by gameChar, and more specifically the coordinates of the pixel at the center of that square.
    if gameDiff == 1:
        gameChar.append(Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),"medChar.gif"))
    elif gameDiff == 2:
        gameChar.append(Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),"hardChar.gif"))
    else:
        gameChar.append(Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),"easyChar.gif"))
    gameChar[2].draw(win)


    #print(gameChar)
    return gameChar

# ====== Generic Function to Move any "Movable Object" ======
# gameChar  : List containing the virtual coordinates of a "moving object" (player character or arrow) and Image object.
# direction : Integer between 0 and 3
# vBoard    : Virtual game board data
# objType   : Integer either 1 or 0, with a default of 0 (0 for player character, 1 for arrow)
def moveGameChar(gameChar,direction,vBoard,objType=0):
##'''
##---------- Character Movement ----------
##The below takes the command for movement and then:
##    1. Undraws the character
##    2. Moves the image file stored the charachters array to the new position
##    3. Draws the character in the new position.
##It also checks to make sure that the player isn't moving off the game board. If
##they are trying to move off the board, it stops them and set the "badMove" flag
##to True.
##If the player has made a bad move, it's passed back to the host handler function.
##'''

    badMove = False
    global gameDiff
    global win
    
    if not objType:
        if gameDiff == 1:
            gamePic = "medChar.gif"
        elif gameDiff == 2:
            gamePic = "hardChar.gif"
        else: gamePic = "easyChar.gif"
    else: gamePic = "gameArrow.gif"

    if direction == 0: # Move up
        try:

            gameChar[2].undraw()
            if (gameChar[1] - 1) >= 0:
                gameChar[1] -= 1
                if objType:
                    print("object Ypos:",gameChar[1])
            else: badMove = True
            gameChar = moveMovObj(vBoard, gameChar, gamePic)

        except:

            badMove = True
            gameChar[1] +=1
        #gameChar[2].draw(win)
        
    elif direction == 1: # Move right
        try:

            gameChar[2].undraw()
            gameChar[0] += 1
            gameChar = moveMovObj(vBoard, gameChar, gamePic)  

        except:

            badMove = True
            gameChar[0] -= 1
        #gameChar[2].draw(win)
        
    elif direction == 2: # Move down
        try:

            gameChar[2].undraw()
            gameChar[1] += 1
            gameChar = moveMovObj(vBoard, gameChar, gamePic)

        except:

            badMove = True
            gameChar[1] -= 1

        #gameChar[2].draw(win)

    elif direction == 3: # Move left
        try:

            gameChar[2].undraw()
            if (gameChar[0] - 1) >= 0:
                gameChar[0] -=1
            else: badMove = True
            gameChar = moveMovObj(vBoard, gameChar, gamePic)
            
        except:

            badMove = True
            gameChar[0] += 1

        #gameChar[2].draw(win)
    #gameChar[2].draw(win)

    return [gameChar,badMove]

# ====== Update the Position of a Given "Movable Object" ======
# vBoard  : Virtual game board data
# movObj  : List containing X and Y virtual coordinates and Image object
# gamePic : String with name of bitmap image ascociated with movObj
def moveMovObj(vBoard,movObj,gamePic):
##'''
##Given a "moving object" (player or arrow), move the it's sprite to the place on the "real" board that corresponds with it's place in the array.
##This function mostly exists to reduce the number of huge, difficult to read array calls that get copy/pasted around so much.
##'''

    # Sets the image object in the moving game object
    movObj[2] = Image(Point(vBoard[movObj[1]][movObj[0]][2][0],vBoard[movObj[1]][movObj[0]][2][1]),gamePic)
    return movObj
    
# ====== Get List of All Non-Moving Objects in The Same Square as a given "Movable Object" ======
# movObj : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# vBoard : Virtual game board data
def whatInSquare(movObj,vBoard):
##'''
##Given a "moving object" (player of arrow), returns a list of what is in the square that they're in.
##    [0] - Wumpus : Boolean True/False
##    [1] - Gold   : Boolean True/False
##    [2] - Pit    : Boolean True/False
##    
##'''
    inSqr = [False,False,False] # Sets default values of what's in the square to 'nothing'
    if vBoard[movObj[1]][movObj[0]][3]:
        inSqr[0] = True
    elif vBoard[movObj[1]][movObj[0]][4]:
        inSqr[1] = True
    elif vBoard[movObj[1]][movObj[0]][5]:
        inSqr[2] = True

    return inSqr
    

# ====== Main Game Window Handler ======
# Does not require anything
def main():
# Despite the name, this is actually just a handler for the main game window.
# Originally, it was the main function, but that role shifted elsewhere.
# However, my laziness has preserved the name.
    
    # doneFlag comes from getDiff(). This is so that if the user closes the difficulty window, the game will not be played.
    doneFlag = getDiff()
    global win # Win is made global so that other functions can write to it.
    global gameDiff # Gamediff is alread created by getDiff()
    win = GraphWin("Hunt The Wumpus",750,502) # Creates game window

    vBoard,deadWumpusList = buildGameGrid(0) # Creates the skeleton game datastructure.
    if len(deadWumpusList) < 2: # If the number of wumpuses is less than 2, it adds a fake entry to deadWumpusList just so that it will be the appropriate size.
        deadWumpusList.append([-1,-1,False])

    gamePoints = 100 # Initializes starting points

    # Based on the chosen difficulty, the cooresponding number of arrows is set up.
    if gameDiff == 0:
        gameArrowCount = 5
    elif gameDiff == 1:
        gameArrowCount = 2
    elif gameDiff == 2:
        gameArrowCount = 2

        ### Creates the text objects which read out sound, points and arrows ###
    reportString = Text(Point(480,315),"Sound:\n-------\n*******")
    reportString.setFace('courier')
    reportString.setSize(12)

    pointsString = Text(Point(645,315),"Points:\n-------\n"+str(gamePoints))
    pointsString.setFace('courier')
    pointsString.setSize(12)

    arrowString = Text(Point(563,390),"Arrows:\n-------\n"+str(gameArrowCount))
    arrowString.setFace('courier')
    pointsString.setSize(12)
   
    # Draws the floor texture
    for rowCnt in vBoard:
        for colCnt in rowCnt:
            Image(Point(colCnt[2][0],colCnt[2][1]),'floor_master.gif').draw(win)

    gameChar = initGameChar(vBoard) # Creates and places the game character


    moveToggle = True # Boolean switch value for whether "movement" or "shoot" mode is engaged (default is move)

    # These are two iterables where the index positions coorespond between them. This is used to easily keep track of buttons in the game and draw them with a compact for loop
    bttnPnts = [[576,50],[636,110],[516,110],[576,170],[55,452],[641,240],[490,240]]
    bttnNames = ["upArrow.gif","rightArrow.gif","leftArrow.gif","downArrow.gif","quit.gif","whiteShoot.gif","blueMove.gif"]

    # Rectangles used to check if the user is clicking on drawn images that serve as buttons
    quitBtn = Rectangle(Point(7,437),Point(103,467))
    upArrow = Rectangle(Point(537,20),Point(597,80))
    rightArrow = Rectangle(Point(606,80),Point(666,140))
    leftArrow = Rectangle(Point(486,80),Point(546,140))
    downArrow = Rectangle(Point(546,140),Point(606,200))
    moveBtn = Rectangle(Point(460,225),Point(520,255))
    shootBtn = Rectangle(Point(609,225),Point(672,255))

    # Because the "move" and "shoot" buttons are drawn over and over, each center point is assigned a variable for easier changes and more readable code.
    moveCntrPnt = Point(490,240)
    shootCntrPnt = Point(641,240)

    # For loop that draws all the buttons onto the game board.
    for point in bttnPnts:
        Image(Point(point[0],point[1]),bttnNames[bttnPnts.index(point)]).draw(win)

    ### DEBUG OPTIONS! ###
    # Uncomment these lines to automatically draw all game items onto the board, including sense data.
    # print("deadWumpusList", len(deadWumpusList))
    # for i in deadWumpusList:
    #     print(i)
    #
    # 
    # ## Draws Wumpus on the Board ##
    # for rowCnt in vBoard:
    #     for colCnt in rowCnt:
    #         if colCnt[3]:
    #             Image(Point(colCnt[2][0],colCnt[2][1]), 'wumpus.gif').draw(win)
    # ## Draws Gold on the Board ##            
    # for rowCnt in vBoard:
    #     for colCnt in rowCnt:
    #         if colCnt[4]:
    #             Image(Point(colCnt[2][0],colCnt[2][1]), 'gold.gif').draw(win)
    #
    # ## Draws Pit on the Board ##            
    # for rowCnt in vBoard:
    #     for colCnt in rowCnt:
    #         if colCnt[5]:
    #             Image(Point(colCnt[2][0],colCnt[2][1]), 'pit.gif').draw(win)

     # A simple test of the correctness of the squares and sense data generated by buildGameGrid
    for rowCnt in vBoard:
        for colCnt in rowCnt:
            #myClick = win.getMouse()
            Rectangle(Point(colCnt[0][0],colCnt[0][1]),Point(colCnt[1][0],colCnt[1][1])).draw(win)
            #print(colCnt[2][0],colCnt[2][1])
            #colCnt[7].draw(win)

    while not doneFlag:
        print(gamePoints)
        print(gameArrowCount)

        ## Every time something is clicked, these variables are re-drawn to the most updated version.
        reportString.undraw()
        reportString.draw(win)

        pointsString.setText("Points:\n-------\n"+str(gamePoints))
        pointsString.undraw()
        pointsString.draw(win)

        arrowString.setText("Arrows:\n-------\n"+str(gameArrowCount))
        arrowString.undraw()
        arrowString.draw(win)

        # pprint(vBoard) # Diagnostic printing of data in a pretty way
        try:
            myClick = win.getMouse()
        except GraphicsError:
            print("graphicsError")
            doneFlag = True

        print(myClick.getX(), myClick.getY())
        
        if not doneFlag:
            if gRectIntersect(quitBtn,myClick):
                print("Quit")
                doneFlag = True

            # If the "move" button is selected. This means pressing the arrows will move the character
            if moveToggle:
                if gRectIntersect(upArrow,myClick):
                    gameChar,gamePoints = moveHandler(gameChar, 0, vBoard, gamePoints,deadWumpusList)
                    print("up arrow")

                elif gRectIntersect(rightArrow,myClick):
                    gameChar,gamePoints = moveHandler(gameChar, 1, vBoard, gamePoints,deadWumpusList)
                    print("right arrow")

                elif gRectIntersect(leftArrow,myClick):
                    gameChar,gamePoints = moveHandler(gameChar, 3, vBoard, gamePoints,deadWumpusList)
                    print("left arrow")

                elif gRectIntersect(downArrow,myClick):
                    gameChar,gamePoints = moveHandler(gameChar, 2, vBoard, gamePoints,deadWumpusList)
                    print("down arrow")

            # If the "move" button is NOT selected (and thus the "shoot" button is selected). Clicking the arrows will shoot an arrow in that direction.
            elif not moveToggle:
                # This will shoot an arrow in the appropriate direction
                if gRectIntersect(upArrow,myClick):
                    gamePoints,gameArrowCount,reportString = arrowHandler(gameChar, 0, vBoard,gamePoints,deadWumpusList,gameArrowCount,reportString)
                    print("fire arrow up")

                elif gRectIntersect(rightArrow,myClick):
                    gamePoints,gameArrowCount,reportString = arrowHandler(gameChar, 1, vBoard, gamePoints,deadWumpusList,gameArrowCount,reportString)
                    print("fire arrow right")

                elif gRectIntersect(leftArrow,myClick):
                    gamePoints,gameArrowCount,reportString = arrowHandler(gameChar, 3, vBoard, gamePoints,deadWumpusList,gameArrowCount,reportString)
                    print("fire arrow left")

                elif gRectIntersect(downArrow,myClick):
                    gamePoints,gameArrowCount,reportString = arrowHandler(gameChar, 2, vBoard, gamePoints,deadWumpusList,gameArrowCount,reportString)
                    print("fire arrow down")
            
            # Move button center point Point(490,240)
            # Shoot button center point: Point(641,240)
            if gRectIntersect(moveBtn,myClick):
                if not moveToggle:
                    # draw the "engaged" moveBtn, then the "disengaged" shootBtn
                    Image(moveCntrPnt,'blueMove.gif').draw(win)
                    Image(shootCntrPnt,'whiteShoot.gif').draw(win)
                    moveToggle = True
            elif gRectIntersect(shootBtn,myClick):
                if moveToggle:
                    # Draw the "disengaged" moveBtn, then the "engaged" shootBtn
                    Image(moveCntrPnt,'whiteMove.gif').draw(win)
                    Image(shootCntrPnt,'blueShoot.gif').draw(win)
                    moveToggle = False

        
    win.close()
    return gamePoints

# ====== Handles the Movement of the Character ======
# gameChar       : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# direction      : Integer between 0 and 3
# vBoard         : Virtual game board data
# gamePoints     : Integer value of the points/score of the game
# deadWumpusList : List containing virtual coordinates of each wumpus, as well as boolean flag for if it's dead or not (True = Dead, False = Alive)
def moveHandler(gameChar, direction, vBoard, gamePoints,deadWumpusList):
# Procedure for Moving the Character:
#     - Get new location of character
#     - Get if the move is good/bad
#     - Retrieve what's in the square you just moved into
#     - Evaluate points:
#         - Deduct 1 point for moving
#         - If move bad, deduct 1 additional point
#         - Check what's in the square you moved into:
#             - If it's a pit
#                 - Deduct 10 points
#             - If it's a dead Wumpus
#                 - If that square has not been visited before
#                     - Add 50 points
#             - If it's a live Wumpus
#                 - Deduct 1000 points
#             - If it's a treasure
#                 - If that square has not been visited before
#                     - Add 100 points
#     - Draw the stack of sprites in the correct order

    global win

    vBoard[gameChar[1]][gameChar[0]][6] = True # Marks the square as having been visited
    # NOTE: This has to be set BEFORE the character is moved so that it doesn't conflict with evaluating the squeare that we're in


    gameChar,badMove = moveGameChar(gameChar,direction,vBoard)

    # inSqr is a list that contains all the the items in a given game square. The structure is as follows
    #   [0] - Wumpus : Boolean (true = is in square)
    #   [1] - Gold   : Boolean (true = is in square)
    #   [2] - Pit    : Boolean (true = is in square)
    inSqr = whatInSquare(gameChar,vBoard)


    ## This sequentially checks if certain items are present in the square, then draws them in the correct order (pit, gold, wumpus).
    ## The game does not undraw anything but the player sprite and the sense string, so board images will tend to accumulate. I'm unaware if that will tend to affect performance.

    if inSqr[2]:
        Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),'pit.gif').draw(win)
    if inSqr[1]:
        Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),'gold.gif').draw(win)
    if inSqr[0]:
        Image(Point(vBoard[gameChar[1]][gameChar[0]][2][0],vBoard[gameChar[1]][gameChar[0]][2][1]),'wumpus.gif').draw(win)
    
    gameChar[2].draw(win)

    # Undraws then draws the sense text on the board.
    vBoard[gameChar[1]][gameChar[0]][7].undraw()
    vBoard[gameChar[1]][gameChar[0]][7].draw(win)

    ## This evaluates and scores the points
    workingPoints = -1
    if badMove: workingPoints -= 1 # Subtracts for invalid move
    if inSqr[2]: workingPoints -= 10 # Subtracts for pit
    if inSqr[1] and not vBoard[gameChar[1]][gameChar[0]][6]: workingPoints += 100 # Adds 100 points for gold
    for wCount in range(len(deadWumpusList)):
        if deadWumpusList[wCount][2]: # Adds 50 points if the Wumpus is dead and the square hasn't been visited before
            
            if deadWumpusList[wCount][0] == gameChar[0] and deadWumpusList[wCount][1] == gameChar[1] and not vBoard[gameChar[1]][gameChar[0]][6]:
                workingPoints += 50
                print('found dead wumpus')

    # This checks:
    #   1. If there is a wumpus in the square you walked into.
    #   2. If that wumpus is alive.
    # If both are True, then you've walked in on a live wumpus and you lose 1000 points :(
    if (deadWumpusList[0][0] == gameChar[0] and deadWumpusList[0][1] == gameChar[1] and not deadWumpusList[0][2]) or (deadWumpusList[1][0] == gameChar[0] and deadWumpusList[1][0] == gameChar[1] and not deadWumpusList[1][2]):
        print('hit live wumpus')
        #pprint(deadWumpusList)
        #pprint(gameChar)
        workingPoints -= 1000

    # Sets the official game points to the working copy    
    gamePoints = gamePoints+workingPoints
    
    return gameChar, gamePoints

# ====== Handles the Firing and Scoring of Arrows ======
# gameChar       : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# direction      : Integer between 0 and 3
# vBoard         : Virtual game board data
# gamePoints     : Integer value of the points/score of the game
# deadWumpusList : List containing virtual coordinates of each wumpus, as well as boolean flag for if it's dead or not (True = Dead, False = Alive)
# gameArrowCount : Integer between 0 and 5 with the number of arrows available to the player.
# reportString   : String with the "sound" heard by the player after firing an arrow
def arrowHandler(gameChar,direction,vBoard,gamePoints,deadWumpusList,gameArrowCount,reportString):
# Arrows are treated in a way similar to how the player is treated. They have a similar data structure, and thus they can be manipulated by the same functions. This makes firing an arrow very easy.
# The arrow-firing process is as follows:
#     1. Spawn in the same square as the player
#     2. Check what is in this square.
#     3. If this square has a wumpus in it:
#         1. If the wumpus is alive:
#             1. Kill it
#             2. Make a "Scream" noise
#             3. Stop moving
#     2. If the wumpus is dead:
#         1. Make a "Plop" noise
#         2. Stop moving
# 4. If you've made a badMove (e.g. Hit a wall):
#     1. Make a "Thunk" noise
#     2. Stop moving
# 5. Try to move to the next square.
# 6. Repeat 2 - 5 till you stop moving.

    gameArrow = [gameChar[0],gameChar[1],"gameArrow.gif"]
    doneFlag = False
    badMove = False
    reportBase = 'Sound:\n-------\n'

    # Initializes the gameArrow variable
    gameArrow[2] = Image(Point(vBoard[gameArrow[1]][gameArrow[0]][2][0],vBoard[gameArrow[1]][gameArrow[0]][2][1]),"gameArrow.gif")

    global win
    
    # Creates a list of what's in the current square
    inSqr = whatInSquare(gameChar,vBoard)

    # Subtract arrows. If you're out of arrows, then you're done.
    if gameArrowCount > 0:
        gameArrowCount -= 1
        gamePoints -= 5
    else:
        doneFlag = True

    # Loop for firing an arrow
    while not doneFlag:
        gameArrow[2].undraw()
        gameArrow[2].draw(win)
        time.sleep(0.5)
        print("BadMove:",badMove)
        #print(gameArrow[0],gameArrow[1])
        
        if badMove:
            reportString.setText(reportBase+"Thunk!")
            doneFlag = True
            print("hit a wall")
        elif inSqr[0]: # If wumpus is in the same square as the arrow

            doneFlag = True
            print("Hit a wumpus")
            #pprint(deadWumpusList)
            for wCount in range(len(deadWumpusList)):
                # print(gameArrow[0],deadWumpusList[wCount][0])
                # print(gameArrow[1],deadWumpusList[wCount][1])
                # print(wCount)

                if deadWumpusList[wCount][0] == gameArrow[0] and deadWumpusList[wCount][1] == gameArrow[1]: # Compares current square to list of dead wumpii

                    print(deadWumpusList[wCount][0], deadWumpusList[wCount][1])
                    if deadWumpusList[wCount][2]: # if you hit a dead wumpus
                        reportString.setText(reportBase+"Plop!")
                    elif not deadWumpusList[wCount][2]: # If you hit a live wumpus
                        deadWumpusList[wCount][2] = True
                        reportString.setText(reportBase+"Scream!")
                        gamePoints += 500
           
        gameArrow,badMove = moveGameChar(gameArrow,direction,vBoard,objType=1)
        inSqr = whatInSquare(gameArrow,vBoard)
        
    gameArrow[2].undraw()
    return gamePoints,gameArrowCount,reportString



# ====== Prompts the User for their Initials ======
def getInitials():
# Prompts the user for a three letter set of initials (must be 3 letters) that does not contain the @ symbol
    
    doneFlag = False

    # Window for entering 
    initialsWin = GraphWin("Enter Your Initials",200,100)

    # The rectangle that will server as the "done" button
    initialDoneBtn = Rectangle(Point(100,33),Point(150,66))
    initialDoneBtn.draw(initialsWin)

    # The entry box for initials
    initialsEntry = Entry(Point(70,50),3)
    initialsEntry.setText("")
    initialsEntry.draw(initialsWin)

    # Text object that goes in the "done" button
    Text(Point(125,49),"Done?").draw(initialsWin)

    # Loop waits for valid user input
    while not doneFlag:
        try:
            myClick = initialsWin.getMouse()
        except GraphicsError:
            doneFlag = True

        #print(myClick.getX(), myClick.getY())
        if not doneFlag:
            isDoneBtnClicked = gRectIntersect(initialDoneBtn,myClick)
            if isDoneBtnClicked:
                initialsText = initialsEntry.getText()
                if len(initialsText) == 3 and "@" not in initialsText:
                    doneFlag = True
                    initialsWin.close()
    eof = False
    return initialsText

# +++++++ Handler for Game Score and High Score File ++++++
def gameHandler():
# Takes the score from the game played by the user
# Reads the existing high scores from file
# If the entered initials are the highest score for that set of initials OR the initials are not yet represented in the high score file, then the high score data is added
# Takes the list of high scores and orders them based on score
# Displays a window that shows the list of top 10 scores
# Writes all scores to file (overwriting the old file)
    
    gameScore = main() # Gamescore retrieved from Main
    global gameDiff # Accesses gamediff

    scoreWin = GraphWin("High Scores!",400,400)

    initialsText = getInitials().upper() # Gets the entered initials from the user.
    print(initialsText)
    
    # NOTE: This file needs to be created.
    myFileName = "lfbWumpusHighScores.txt"
    

    myFile = open(myFileName, 'r') # Opens the file to read

    eof = False # Used to flag the end of a file.
    #print('got to open file')
    # The structure of the highscores file is as follows:
    # Each line contaings the following data:
    #   0 - High score (integer)
    #   1 - Game Difficulty (integer)
    #   2 - Initials (string)
    # Each of these values will occur on each line in that order, delimited by the "@" symbol
    print("")
    scoreList = []
    while not eof:
        txtLine = myFile.readline()
        print('txtLine',txtLine)
        if len(txtLine) > 0:
            print("txtLine",txtLine)
            scoreList.append((txtLine.strip()).split('@')) # Strips the newline and splits on the @

        else: eof = True

    eof = False

    myFile.close() # Closes the file to avoid later conflict
    #pprint(scoreList)
    scoreLsCopy = scoreList # Working copy of scoreList
    appendFlag = True # Flag for appending new score

    for entry in scoreLsCopy:
        scoreList[scoreLsCopy.index(entry)][0] = eval(entry[0])
        scoreList[scoreLsCopy.index(entry)][1] = eval(entry[1])

    scoreLsCopy = scoreList # Resets as working copy again

    # This loop ensures one entry per set of initials, and that that entry is the largest of all the ones entered.
    for entry in scoreLsCopy:
        if initialsText == entry[2]:
            if gameScore >= entry[0]:
                del(scoreList[scoreList.index(entry)]) # If the initials exist and are asscociated with a lower score, delete them from the list
            elif gameScore < entry[0]: # If the same initails are assciciated with a higher score, then don't display the given score
                appendFlag = False

    if appendFlag:
        scoreList.append([gameScore,gameDiff,initialsText])

    # Creates topList as working copy of scoreList
    topList = sorted(scoreList,reverse=True) # Automatically sorts by score, from highest to lowest
    topList = topList[0:10] # Limits the scoreList to the top 10 scores

    # Will be the string that shows the nice scores
    printScores = "|  Score  | Difficulty | Initials |\n"

    for stuff in topList:
        if stuff[2] == 0:
            diffString = "Easy"
        elif stuff[2] == 1:
            diffString = "Medium"
        elif stuff[2] == 2:
            diffString = "Hard"
        printScores += "{0:^10}{1:^14}{2:^7}\n".format(stuff[0],stuff[1],stuff[2])

    print(printScores)
    printScores = Text(Point(200,200),printScores)
    printScores.setFace('courier')
    printScores.setSize(12)
    printScores.draw(scoreWin)

    myFile = open(myFileName,'w')
    scoreLsCopy = "" # Reassignment for compaction

    for stuff in scoreList:
        scoreLsCopy += str(stuff[0])+'@'+str(stuff[1])+'@'+str(stuff[2])+'\n'

    myFile.write(scoreLsCopy)

    while not eof:
        try:
            myClick = scoreWin.getMouse()
        except: eof = True
    scoreWin.close()

gameHandler()

#btnSize()
