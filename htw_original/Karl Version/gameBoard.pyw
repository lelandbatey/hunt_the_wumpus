from graphics import *

def gPtDist(myPt1,myPt2):
    Xpt1,Ypt1 = myPt1.getX(),myPt1.getY()
    Xpt2,Ypt2 = myPt2.getX(),myPt2.getY()
    dist=((Xpt1-Xpt2)**2+(Ypt1-Ypt2)**2)**0.5
    return dist

def gCircInt(myCircle,myPt):
    inCirc = False
    circCent,circRad = myCircle.getCenter(),myCircle.getRadius()
    dist = gPtDist(circCent,myPt)
    if dist<=circRad:
        inCirc = True
    return inCirc

def board():
    win = GraphWin("Hunt the Wumpus",600,400)
    boardSize = 8
    sqX,sqY = 0,0
    numSq = boardSize**2
    sqSize = 400/boardSize
    sqList = []
    tileList = []
    
    for iRow in range(boardSize):
        tmpRow,tmpTile = [],[]
        for iCol in range(boardSize):
            centPt = Point((iCol+0.5)*sqSize,(iRow+0.5)*sqSize)
            tmpRow.append(centPt)
            floorTile = Image(centPt,"floor_master.gif")
            floorTile.draw(win) # temp, draws all tiles at initial
            tmpTile.append(floorTile)
        sqList.append(tmpRow)
        tileList.append(tmpTile)
		
        title = Image(Point(500,50),"titleLogo.gif")
        title.draw(win)
	
        arrows = Image(Point(505,175),"arrows.gif")
        arrows.draw(win)

        arrowUp = Circle(Point(505,118),25)
        arrowRt = Circle(Point(562,175),25)
        arrowLt = Circle(Point(448,175),25)
        arrowDn = Circle(Point(505,232),25)
        turnBtn = Circle(Point(505,175),25)

    hunterX = 0
    hunterY = 0
    hunter = Image(sqList[hunterY][hunterX],"hunterFrontEasy.gif")
    hunter.draw(win)
    turnFlag = 3

    doneFlag = False
	
    while not doneFlag:        
		
        try: mc = win.getMouse()
        except: doneFlag = True

        if gCircInt(arrowUp,mc):
            if hunterY > 0:
                hunter.undraw()
                hunterY -= 1
                hunter = Image(sqList[hunterY][hunterX],"hunterBackEasy.gif")
                hunter.draw(win)
                turnFlag = 1
                print("up")
            else: print("penalty")

        if gCircInt(arrowRt,mc):
            if hunterX < boardSize-1:
                hunter.undraw()
                hunterX += 1
                hunter = Image(sqList[hunterY][hunterX],"hunterRightEasy.gif")
                hunter.draw(win)
                turnFlag = 2
                print("right")
            else: print("penalty")

        if gCircInt(arrowDn,mc):
            if hunterY < boardSize-1:
                hunter.undraw()
                hunterY += 1
                hunter = Image(sqList[hunterY][hunterX],"hunterFrontEasy.gif")
                hunter.draw(win)
                turnFlag = 3
                print("down")
            else: print("penalty")

        if gCircInt(arrowLt,mc):
            if hunterX > 0:
                hunter.undraw()
                hunterX -= 1
                hunter = Image(sqList[hunterY][hunterX],"hunterLeftEasy.gif")
                hunter.draw(win)
                turnFlag = 4
                print("left")
            else: print("penalty")

        if gCircInt(turnBtn,mc):
            if turnFlag == 1: # facing away
                hunter.undraw()
                hunter = Image(sqList[hunterY][hunterX],"hunterRightEasy.gif")
                hunter.draw(win)
                turnFlag = 2 # facing right
            elif turnFlag == 2: # facing right
                hunter.undraw()
                hunter = Image(sqList[hunterY][hunterX],"hunterFrontEasy.gif")
                hunter.draw(win)
                turnFlag = 3 # facing front
            elif turnFlag == 3: # facing front
                hunter.undraw()
                hunter = Image(sqList[hunterY][hunterX],"hunterLeftEasy.gif")
                hunter.draw(win)
                turnFlag = 4 # facing left
            elif turnFlag == 4: # facing left
                hunter.undraw()
                hunter = Image(sqList[hunterY][hunterX],"hunterBackEasy.gif")
                hunter.draw(win)
                turnFlag = 1 # facing away
            print("turn")

    win.close()

board()
