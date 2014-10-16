# Makes printing work correctly in Python 2.x
# Has to be up at the top of the file
from __future__ import print_function
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



ADDENDUM
--------
This is labeled the "cleaned up" version, but that doesn't mean the structure
has been changed much (if at all). All I've attempted to do is to improve the
styling of the code so it more closely follows PEP 8. It'll make it *slightly*
less painful to read.

The only non-style changes I've made are ones like appending nearby folders to
the path to make running this more convenient.
'''
# For importing "graphics.py"
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')


try:
    from graphics import *
except:
    print("Error: Need the library 'graphics.py' to run.")
    print("       Search online for it, and put it in this folder.")
from random import randint
from pprint import pprint
import time

# Defined at the module level, but left empty. It's first actually assigned a
# value in `main()`
MAIN_WINDOW = None
GAMEDIFF = 0
# ====== Get Difficulty ======
# Presents the user with a window for selecting the difficulty
# (easy, medium or hard)
#   Represented as a single integer:
#   0 - Easy
#   1 - Medium
#   2 - Hard
#
#   This data is storred in the global variable "GAMEDIFF"
def get_diff():
    """Presents the user with a window for selecting the difficulty."""
    global GAMEDIFF
    diff = GraphWin("Choose the difficulty!", 400, 100)
    done_flag = False
    easy_btn = Rectangle(Point(66, 36), Point(134, 64))
    medium_btn = Rectangle(Point(166, 36), Point(234, 64))
    hard_btn = Rectangle(Point(266, 36), Point(334, 64))
    button_points = [[100, 50], [200, 50], [300, 50]]
    button_names = ["easybutton.gif", 'mediumbutton.gif', 'hardbutton.gif']
    for point in button_points:
        Image(Point(point[0], point[1]), \
            button_names[button_points.index(point)]).draw(diff)

    # Quitgame is a variable that catches whether the user clicked the red x
    # button on the "choose difficulty" window. The "main()" function uses it
    # to define "done_flag so that it will end the game at that."
    quit_game = False

    while not done_flag:
        try:
            my_click = diff.getMouse()
        except GraphicsError:
            quit_game = True
            done_flag = True
            GAMEDIFF = 0
        if not done_flag:
            if get_rect_intersect(easy_btn, my_click):
                print("Easy")
                GAMEDIFF = 0
                done_flag = True 
            elif get_rect_intersect(medium_btn, my_click):
                print("Medium")
                GAMEDIFF = 1
                done_flag = True
            if get_rect_intersect(hard_btn, my_click):
                print("Hard")
                GAMEDIFF = 2
                done_flag = True
    diff.close()
    return quit_game
    
# ====== Check if Click is Inside Rectangle ======
# Requires that a Rectangle and Point object be passed
#
# Checks to see if the point (presumed to be the user's mouse click) falls
# within the area of the given Rectangle object
#
# Written by Russel Swannack
# Used with permission.
def get_rect_intersect(my_rectangle, my_point):
    """Given a rectangle and point, check if the point is in the rectangle."""
    # Need to account for the possibility that the rectangle was constructed
    # backwards
    pnt_1x = min(my_rectangle.getP1().getX(), my_rectangle.getP2().getX())
    pnt_2x = max(my_rectangle.getP1().getX(), my_rectangle.getP2().getX())
    pnt_1y = min(my_rectangle.getP1().getY(), my_rectangle.getP2().getY())
    pnt_2y = max(my_rectangle.getP1().getY(), my_rectangle.getP2().getY())

    # Get Test Point Info
    test_pnt_x, test_pnt_y = my_point.getX(), my_point.getY()

    # Check to see if the test point is within the rectangle bounds
    is_within = test_pnt_x >= pnt_1x \
    and test_pnt_x <= pnt_2x \
    and test_pnt_y >= pnt_1y \
    and test_pnt_y <= pnt_2y
    
    return is_within

# ====== Building The Game Data Skeleton ======
# top_left_pnt   : List with two entries, the X and Y (in that order) pixel points of the top left point #pylint: disable=C0301, C0301
# pixel_count    : Integer of number of pixels wide that the board must be (defaults to 400)
def build_game_grid(top_left_pnt=[2, 2], pixel_count=400):
    """Creates an empty game grid structure."""
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
##        "S B G" - "stench, " "breaze, " and "Glitter" in that order.
##        If one of these is not present it will be replaced with a "-" character to signify no sense of that kind.
##
##This loop will initially only fill the first three values (upper left, lower right, and center point coordinates).
##All other values will be set to default values (False for booleans, "-" for strings). These other values will be
##calculated in other modules.'''

    # Accesses the global variable for the level of difficulty
    global GAMEDIFF 
    
    # Based on the difficulty of this game instance, squares_count is set to the appropriate value
    # squares_count represents the number of squares in each row and column of the game board. Because the game board is a square, the number of rows and columns is the same, thus there is only one value for both.
    if GAMEDIFF == 0:
        squares_count = 8
    elif GAMEDIFF == 1:
        squares_count = 9
    elif GAMEDIFF == 2:
        squares_count = 10

    # Alright, this is a super hack to fix stuff some problems that I'm having, but I don't care
    #squares_count += 1
    
    div_factor = pixel_count//squares_count

    prior_point = top_left_pnt

    # grid_list will be the final array
    grid_list, tmp_list, low_rt_tmp, centr_pnt_tmp = [], [], [], []

    for row_count in range(squares_count):
        grid_list.append([])
        for column_count in range(squares_count):
            # Calculates lower right point of the game square.
            low_rt_tmp = [prior_point[0]+div_factor, prior_point[1]+div_factor] 
            # calculates the center point
            centr_pnt_tmp = [int(prior_point[0]+div_factor/2), int(prior_point[1]+div_factor/2)] 

            # vvv - That command appends everything to the list, including default values for what the square contains and what you sense when entering this square.
            #tmp_list.append(prior_point, low_rt_tmp, centr_pnt_tmp, False, False, False, False, "- - -")
            for i in [prior_point, low_rt_tmp, centr_pnt_tmp, False, False, False, False, Text(Point(centr_pnt_tmp[0], centr_pnt_tmp[1] - (15/10*squares_count)), "- - -")]:
                tmp_list.append(i)
            grid_list[row_count].append(tmp_list)

            # Iterates prior point to the next point
            prior_point = [prior_point[0]+div_factor, prior_point[1]] 
            tmp_list = []

        # Resets prior_point, but increments the Y to the beginning of the next row
        prior_point = [top_left_pnt[0], (row_count+1)*div_factor+2] 

    # Sets up the location of game elements like treasure, wumpus, etc
    grid_list, dead_wumpus_lst = place_game_elements(grid_list, GAMEDIFF)
    
    return grid_list, dead_wumpus_lst


# ====== Create List of Random Points ======
#
# Requires minimum and maximum values for the randomly generated numbers, as
# well as the total amount of random integers to be generated.
#
# This function was written by Russell Swannack for Cpts 111 HW 09 - Q 04
# Modified and used with permission
def get_rand_pnts_list(imin, imax, itotal):
    """Returns given number of randomly generate xy pairs."""
    xy_lst = [] # Initialize the List
    # Keep looping until we have the number of required XY pairs
    while len(xy_lst) < itotal: 
        # Create a random XY Pair
        tmp_xy = [randint(imin, imax), randint(imin, imax)]
        # If it is not already in the list, append it to the list
        if not tmp_xy in xy_lst:
            xy_lst.append(tmp_xy)
    return xy_lst

# ====== Sets Random Positions of Game Objects ======
#
# Based on the difficulty, this places game objects (wumpus, pit, gold) on the
# virtual game board (virtual_board) by setting the appropriate flags in the
# selected squares to True
#
# Requires that the game board and difficulty be passes (if the difficulty is
# not passed, it defaults to a difficulty of 1)
def place_game_elements(virtual_board, difficulty=1):
    """Randomly places game elements on a virtual_board structure."""

    # A list which shall containg 2 lists:
    #   Each sub-list will contain the virtual X and Y coordinates of a wumpus
    #   on the game board, as well as a boolean value which keeps track of
    #   whether that wumpus is alive or dead (False = Alive, True = Dead)
    dead_wumpus_lst = []


    # Based on the provided difficulty, the game sets the number of pits,
    # treasures, and wumpii to be placed on the game board.
    if difficulty == 0:
        pits = randint(10, 15)
        treasure = randint(10, 15)
        wumpus = 1
        squares_count = 7
    elif difficulty == 1:
        pits = randint(15, 20)
        treasure = randint(10, 15)
        wumpus = 1
        squares_count = 8
    elif difficulty == 2:
        pits = randint(15, 20)
        treasure = randint(15, 20)
        wumpus = 2
        # Set one lower than normal to account for list beginning at 0
        squares_count = 9 
    else: print("difficulty error")

    # Each <object>Points variable is a list containing an appropriate number of sub-lists of the virtual coordinates where a game object will be placed on the vitual game board.
    pit_pnts = get_rand_pnts_list(0, squares_count, pits)
    treasure_pnts = get_rand_pnts_list(0, squares_count, treasure)
    wumpus_pnts = get_rand_pnts_list(0, squares_count, wumpus)

    # Iterates through each list of points of game objects, then changes the corresponding value in the given game square
    for coords in pit_pnts:
        virtual_board[coords[0]][coords[1]][5] = True
    for coords in treasure_pnts:
        virtual_board[coords[0]][coords[1]][4] = True
    for coords in wumpus_pnts:
        virtual_board[coords[0]][coords[1]][3] = True
        dead_wumpus_lst.append([coords[1], coords[0], False])

    virtual_board = set_senses(virtual_board)
    
    return virtual_board, dead_wumpus_lst

# ====== Sets the Sense Data for Each Game Square ======
# Requires the virtual board data (virtual_board)
def set_senses(virtual_board):
    """Set's the "senses" string of each square on the virtual_board"""
    #"""
    #Looks at the board, and checks if an adjacent square has a game object in it (wumpus, treasure, or pit).
    #If there is a game object next to it, then it set's it's own "sense" attribute accordingly.
    #"""

    # Each of these numbers is the position in the gameSquare objects data list.
    #   For example, the item in position 5 in a gameSquares attribute list will always contain the boolean value for whether that gameSquare has a pit in it.
    pit = 5
    treasure = 4
    wump = 3
    
    for row_count in range(len(virtual_board)):
        # Resets sense data for this loop
        stench = False
        glitter = False
        breeze = False
        for column_count in range(len(virtual_board)):
            # Resets sense data for this loop
            stench = False
            glitter = False
            breeze = False
            sense_str = ""

            # Checks all adjacent rows for game objects
            # try:
            #     if virtual_board[abs(row_count-1)][column_count][pit] or virtual_board[row_count][abs(column_count-1)][pit] or virtual_board[abs(row_count+1)][column_count][pit] or virtual_board[row_count][abs(column_count+1)][pit]:
            #         breeze = True
            # except: pass
            # try:
            #     if virtual_board[abs(row_count-1)][column_count][treasure] or virtual_board[row_count][abs(column_count-1)][treasure] or virtual_board[abs(row_count+1)][column_count][treasure] or virtual_board[row_count][abs(column_count+1)][treasure]:
            #         glitter = True
            # except: pass
            # try:
            #     if virtual_board[abs(row_count-1)][column_count][wump] or virtual_board[row_count][abs(column_count-1)][wump] or virtual_board[abs(row_count+1)][column_count][wump] or virtual_board[row_count][abs(column_count+1)][wump]:
            #         stench = True
            # except: pass

            # For this square, checks if an adjacent square has a pit, gold, or wumpus in it, then sets the appropriate boolean value
            breeze = get_adjacent([column_count, row_count], virtual_board, pit)
            glitter = get_adjacent([column_count, row_count], virtual_board, treasure)
            stench = get_adjacent([column_count, row_count], virtual_board, wump)


            # Based on the sense evaluation above, builds the sense_str
            if stench:
                sense_str += "S "
            else: sense_str += "- "
            
            if breeze:
                sense_str += "B "
            else: sense_str += "- "

            if glitter:
                sense_str += "G"
            else: sense_str += "-"

            # Sets the correct Text object for this square, as well as it's text color, size and typeface
            virtual_board[row_count][column_count][7].setText(sense_str)
            virtual_board[row_count][column_count][7].setFace('courier')
            virtual_board[row_count][column_count][7].setSize(6)
            virtual_board[row_count][column_count][7].setTextColor('white')

    return virtual_board


# ====== Generic Function for Finding the Objects in Adjacent Squares =======
# vcoords : Virtual coordinates of the game square
# virtual_board  : Virtual game board data
# obj     : Integer which is reference to game object flag in game square data in virtual_board. 3, 4, and 5 are valid values.
def get_adjacent(vcoords, virtual_board, obj):
    """Generic function for finding the objects in adjacent squares"""
## vcoords is a list with the X and Y virtual points of the location of a square on the gameBoard
## This was written to more elegantly handle the problem of finding the correct objects around a square.
    sense = False
    try:
        if virtual_board[abs(vcoords[1]-1)][vcoords[0]][obj]:
            sense = True
    except:
        print("row_count:", vcoords[1], "column_count:", vcoords[0], "Checking: Row - 1")
    
    try:
        if virtual_board[vcoords[1]][abs(vcoords[0]-1)][obj]:
            sense = True
    except:
        print("row_count:", vcoords[1], "column_count:", vcoords[0], "Checking: Col - 1")
    
    try:
        if virtual_board[vcoords[1]+1][vcoords[0]][obj]:
            sense = True
    except:
        print("row_count:", vcoords[1], "column_count:", vcoords[0], "Checking: Row + 1")
    
    try:
        if virtual_board[vcoords[1]][vcoords[0]+1][obj]:
            sense = True
    except:
        print("row_count:", vcoords[1], "column_count:", vcoords[0], "Checking: Col + 1")

    return sense


# ====== NON-IMPLEMENTED FUNCTION ======
# This function is not actually used anywhere in the program. However, it was
# used during development to make the placement of buttons and rectangles
# easier.
def buttn_size():
    """Function for finding the size of a button."""
    # I wrote this so I won't have to do so much tedious math to get the points for rectangles for buttons.
    btnw = eval(input("Button width: "))
    btnh = eval(input("Button height: "))
    btnCentX, btnCentY = eval(input("Button center point X and Y, command separated: "))
    print("Top left point : ", btnCentX-(btnw/2), btnCentY-(btnh/2))
    print("Lower right point: ", btnCentX+btnw/2, btnCentY+btnh/2)
    print("Rectangle(Point("+str(int(btnCentX-(btnw/2)))+", "+str(int(btnCentY-(btnh/2)))+"), Point("+str(int(btnCentX+btnw/2))+", "+str(int(btnCentY+btnh/2))+"))")

# ====== Initailizing the Game Character ======
# virtual_board : Virtual game board data
def initialize_game_character(virtual_board, game_chr=[]): #pylint: disable=W0102
    """Initializes the game character."""
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
    global MAIN_WINDOW
    global GAMEDIFF


    # This loop iterates through the game board, checking to see if the current space is empty. If it is, it sets the character's position to that square. However, it continues the process, repeatedly setting the players position to every blank sqare. Because of this, the player will have  a tendency to be placed in teh lower right corner of the board.
    print(len(virtual_board))
    for row_count in virtual_board:
        for column_count in row_count:
            if not column_count[3] and not column_count[4] and not column_count[5]:
                game_chr = [row_count.index(column_count), virtual_board.index(row_count)]
    print(game_chr)

    # The long array reference refers to the virtual square inhabited by game_chr, and more specifically the coordinates of the pixel at the center of that square.
    if GAMEDIFF == 1:
        game_chr.append(Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], \
            virtual_board[game_chr[1]][game_chr[0]][2][1]), "medChar.gif"))
    elif GAMEDIFF == 2:
        game_chr.append(Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], \
            virtual_board[game_chr[1]][game_chr[0]][2][1]), "hardChar.gif"))
    else:
        game_chr.append(Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], \
            virtual_board[game_chr[1]][game_chr[0]][2][1]), "easyChar.gif"))
    game_chr[2].draw(MAIN_WINDOW)

    #print(game_chr)
    return game_chr

# ====== Generic Function to Move any "Movable Object" ======
# game_chr  : List containing the virtual coordinates of a "moving object" (player character or arrow) and Image object.
# direction : Integer between 0 and 3
# virtual_board    : Virtual game board data
# objType   : Integer either 1 or 0, with a default of 0 (0 for player character, 1 for arrow)

def move_game_character(game_chr, direction, virtual_board, objType=0):
    """Moves a character structure around the virtual_board."""
##'''
##---------- Character Movement ----------
##The below takes the command for movement and then:
##    1. Undraws the character
##    2. Moves the image file stored the characters array to the new position
##    3. Draws the character in the new position.
##It also checks to make sure that the player isn't moving off the game board. If
##they are trying to move off the board, it stops them and set the "bad_move" flag
##to True.
##If the player has made a bad move, it's passed back to the host handler function.
##'''

    bad_move = False
    global GAMEDIFF
    global MAIN_WINDOW
    
    if not objType:
        if GAMEDIFF == 1:
            game_pic = "medChar.gif"
        elif GAMEDIFF == 2:
            game_pic = "hardChar.gif"
        else: game_pic = "easyChar.gif"
    else: game_pic = "gameArrow.gif"

    if direction == 0: # Move up
        try:

            game_chr[2].undraw()
            if (game_chr[1] - 1) >= 0:
                game_chr[1] -= 1
                if objType:
                    print("object Ypos:", game_chr[1])
            else: bad_move = True
            game_chr = move_mov_obj(virtual_board, game_chr, game_pic)

        except:
            bad_move = True
            game_chr[1] += 1
        #game_chr[2].draw(MAIN_WINDOW)
        
    elif direction == 1: # Move right
        try:

            game_chr[2].undraw()
            game_chr[0] += 1
            game_chr = move_mov_obj(virtual_board, game_chr, game_pic)  

        except:

            bad_move = True
            game_chr[0] -= 1
        #game_chr[2].draw(MAIN_WINDOW)
        
    elif direction == 2: # Move down
        try:

            game_chr[2].undraw()
            game_chr[1] += 1
            game_chr = move_mov_obj(virtual_board, game_chr, game_pic)

        except:

            bad_move = True
            game_chr[1] -= 1

        #game_chr[2].draw(MAIN_WINDOW)

    elif direction == 3: # Move left
        try:

            game_chr[2].undraw()
            if (game_chr[0] - 1) >= 0:
                game_chr[0] -= 1
            else: bad_move = True
            game_chr = move_mov_obj(virtual_board, game_chr, game_pic)
            
        except:

            bad_move = True
            game_chr[0] += 1

        #game_chr[2].draw(MAIN_WINDOW)
    #game_chr[2].draw(MAIN_WINDOW)

    return [game_chr, bad_move]

# ====== Update the Position of a Given "Movable Object" ======
# virtual_board  : Virtual game board data
# move_obj  : List containing X and Y virtual coordinates and Image object
# game_pic : String with name of bitmap image ascociated with move_obj
def move_mov_obj(virtual_board, move_obj, game_pic):
    '''Move a "moving object" (player or arrow) to the place inthe given array.
    
    This function mostly exists to reduce the number of huge, difficult to
    read array calls that get copy/pasted around so much. '''

    # Sets the image object in the moving game object
    move_obj[2] = Image(Point(virtual_board[move_obj[1]][move_obj[0]][2][0], \
        virtual_board[move_obj[1]][move_obj[0]][2][1]), game_pic)
    return move_obj
    
# ====== Get List of All Non-Moving Objects in The Same Square as a given "Movable Object" ======
# move_obj : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# virtual_board : Virtual game board data
def what_in_square(move_obj, virtual_board):
    '''Given a "moving object" (player of arrow), returns a list of what is in the square that they're in.

    Format of the return value:

       [0] - Wumpus : Boolean True/False
       [1] - Gold   : Boolean True/False
       [2] - Pit    : Boolean True/False   
    '''

    # Sets default values of what's in the square to 'nothing'
    in_sqr = [False, False, False]
    if virtual_board[move_obj[1]][move_obj[0]][3]:
        in_sqr[0] = True
    elif virtual_board[move_obj[1]][move_obj[0]][4]:
        in_sqr[1] = True
    elif virtual_board[move_obj[1]][move_obj[0]][5]:
        in_sqr[2] = True

    return in_sqr
    

# ====== Main Game Window Handler ======
# Does not require anything
def main():
    """Main game window handler."""
# Despite the name, this is actually just a handler for the main game window.
# Originally, it was the main function, but that role shifted elsewhere.
# However, my laziness has preserved the name.
    
    # done_flag comes from get_diff(). This is so that if the user closes the difficulty window, the game will not be played.
    done_flag = get_diff()

    # MAIN_WINDOW is made global so that other functions can write to it.
    global MAIN_WINDOW
    # Creates game window
    MAIN_WINDOW = GraphWin("Hunt The Wumpus", 750, 502) 
    
    # GAMEDIFF is already created by get_diff()
    global GAMEDIFF

    # Creates the skeleton game data-structure.
    virtual_board, dead_wumpus_lst = build_game_grid()
    # If the number of wumpuses is less than 2, it adds a fake entry to
    # dead_wumpus_lst just so that it will be the appropriate size.
    if len(dead_wumpus_lst) < 2: 
        dead_wumpus_lst.append([-1, -1, False])

    game_points = 100 # Initializes starting points

    # Based on the chosen difficulty, the cooresponding number of arrows is set up.
    if GAMEDIFF == 0:
        game_arrow_count = 5
    elif GAMEDIFF == 1:
        game_arrow_count = 2
    elif GAMEDIFF == 2:
        game_arrow_count = 2

        ### Creates the text objects which read out sound, points and arrows ###
    report_str = Text(Point(480, 315), "Sound:\n-------\n*******")
    report_str.setFace('courier')
    report_str.setSize(12)

    points_str = Text(Point(645, 315), "Points:\n-------\n"+str(game_points))
    points_str.setFace('courier')
    points_str.setSize(12)

    arrow_str = Text(Point(563, 390), "Arrows:\n-------\n"+str(game_arrow_count))
    arrow_str.setFace('courier')
    points_str.setSize(12)
   
    # Draws the floor texture
    for row_count in virtual_board:
        for column_count in row_count:
            Image(Point(column_count[2][0], column_count[2][1]), 'floor_master.gif').draw(MAIN_WINDOW)

    game_chr = initialize_game_character(virtual_board) # Creates and places the game character


    # Boolean switch value for whether "movement" or "shoot" mode is engaged
    # (default is move)
    mv_toggle = True

    # These are two iterables where the index positions coorespond between them. This is used to easily keep track of buttons in the game and draw them with a compact for loop
    button_points = [[576, 50], [636, 110], [516, 110], [576, 170], [55, 452], [641, 240], [490, 240]]
    button_names = ["upArrow.gif", "rightArrow.gif", "leftArrow.gif", "downArrow.gif", "quit.gif", "whiteShoot.gif", "blueMove.gif"]

    # Rectangles used to check if the user is clicking on drawn images that serve as buttons
    quit_bt = Rectangle(Point(7, 437), Point(103, 467))
    up_arrow = Rectangle(Point(537, 20), Point(597, 80))
    right_arrow = Rectangle(Point(606, 80), Point(666, 140))
    left_arrow = Rectangle(Point(486, 80), Point(546, 140))
    down_arrow = Rectangle(Point(546, 140), Point(606, 200))
    mv_btn = Rectangle(Point(460, 225), Point(520, 255))
    shoot_btn = Rectangle(Point(609, 225), Point(672, 255))

    # Because the "move" and "shoot" buttons are drawn over and over, each center point is assigned a variable for easier changes and more readable code.
    mv_center_point = Point(490, 240)
    shoot_center_point = Point(641, 240)

    # For loop that draws all the buttons onto the game board.
    for point in button_points:
        Image(Point(point[0], point[1]), button_names[button_points.index(point)]).draw(MAIN_WINDOW)

    ### DEBUG OPTIONS! ###
    # Uncomment these lines to automatically draw all game items onto the board, including sense data.
    # print("dead_wumpus_lst", len(dead_wumpus_lst))
    # for i in dead_wumpus_lst:
    #     print(i)
    #
    # 
    # ## Draws Wumpus on the Board ##
    # for row_count in virtual_board:
    #     for column_count in row_count:
    #         if column_count[3]:
    #             Image(Point(column_count[2][0], column_count[2][1]), 'wumpus.gif').draw(MAIN_WINDOW)
    # ## Draws Gold on the Board ##            
    # for row_count in virtual_board:
    #     for column_count in row_count:
    #         if column_count[4]:
    #             Image(Point(column_count[2][0], column_count[2][1]), 'gold.gif').draw(MAIN_WINDOW)
    #
    # ## Draws Pit on the Board ##            
    # for row_count in virtual_board:
    #     for column_count in row_count:
    #         if column_count[5]:
    #             Image(Point(column_count[2][0], column_count[2][1]), 'pit.gif').draw(MAIN_WINDOW)

     # A simple test of the correctness of the squares and sense data generated by build_game_grid
    for row_count in virtual_board:
        for column_count in row_count:
            #my_click = MAIN_WINDOW.getMouse()
            Rectangle(Point(column_count[0][0], column_count[0][1]), Point(column_count[1][0], column_count[1][1])).draw(MAIN_WINDOW)
            #print(column_count[2][0], column_count[2][1])
            #column_count[7].draw(MAIN_WINDOW)

    while not done_flag:
        print(game_points)
        print(game_arrow_count)

        ## Every time something is clicked, these variables are re-drawn to the most updated version.
        report_str.undraw()
        report_str.draw(MAIN_WINDOW)

        points_str.setText("Points:\n-------\n"+str(game_points))
        points_str.undraw()
        points_str.draw(MAIN_WINDOW)

        arrow_str.setText("Arrows:\n-------\n"+str(game_arrow_count))
        arrow_str.undraw()
        arrow_str.draw(MAIN_WINDOW)

        # pprint(virtual_board) # Diagnostic printing of data in a pretty way
        try:
            my_click = MAIN_WINDOW.getMouse()
        except GraphicsError:
            print("graphicsError")
            done_flag = True

        print(my_click.getX(), my_click.getY())
        
        if not done_flag:
            if get_rect_intersect(quit_bt, my_click):
                print("Quit")
                done_flag = True

            # If the "move" button is selected. This means pressing the arrows will move the character
            if mv_toggle:
                if get_rect_intersect(up_arrow, my_click):
                    game_chr, game_points = move_handler(game_chr, 0, virtual_board, game_points, dead_wumpus_lst)
                    print("up arrow")

                elif get_rect_intersect(right_arrow, my_click):
                    game_chr, game_points = move_handler(game_chr, 1, virtual_board, game_points, dead_wumpus_lst)
                    print("right arrow")

                elif get_rect_intersect(left_arrow, my_click):
                    game_chr, game_points = move_handler(game_chr, 3, virtual_board, game_points, dead_wumpus_lst)
                    print("left arrow")

                elif get_rect_intersect(down_arrow, my_click):
                    game_chr, game_points = move_handler(game_chr, 2, virtual_board, game_points, dead_wumpus_lst)
                    print("down arrow")

            # If the "move" button is NOT selected (and thus the "shoot" button is selected). Clicking the arrows will shoot an arrow in that direction.
            elif not mv_toggle:
                # This will shoot an arrow in the appropriate direction
                if get_rect_intersect(up_arrow, my_click):
                    game_points, game_arrow_count, report_str = arrow_handler(game_chr, 0, virtual_board, game_points, dead_wumpus_lst, game_arrow_count, report_str)
                    print("fire arrow up")

                elif get_rect_intersect(right_arrow, my_click):
                    game_points, game_arrow_count, report_str = arrow_handler(game_chr, 1, virtual_board, game_points, dead_wumpus_lst, game_arrow_count, report_str)
                    print("fire arrow right")

                elif get_rect_intersect(left_arrow, my_click):
                    game_points, game_arrow_count, report_str = arrow_handler(game_chr, 3, virtual_board, game_points, dead_wumpus_lst, game_arrow_count, report_str)
                    print("fire arrow left")

                elif get_rect_intersect(down_arrow, my_click):
                    game_points, game_arrow_count, report_str = arrow_handler(game_chr, 2, virtual_board, game_points, dead_wumpus_lst, game_arrow_count, report_str)
                    print("fire arrow down")
            
            # Move button center point Point(490, 240)
            # Shoot button center point: Point(641, 240)
            if get_rect_intersect(mv_btn, my_click):
                if not mv_toggle:
                    # draw the "engaged" mv_btn, then the "disengaged" shoot_btn
                    Image(mv_center_point, 'blueMove.gif').draw(MAIN_WINDOW)
                    Image(shoot_center_point, 'whiteShoot.gif').draw(MAIN_WINDOW)
                    mv_toggle = True
            elif get_rect_intersect(shoot_btn, my_click):
                if mv_toggle:
                    # Draw the "disengaged" mv_btn, then the "engaged" shoot_btn
                    Image(mv_center_point, 'whiteMove.gif').draw(MAIN_WINDOW)
                    Image(shoot_center_point, 'blueShoot.gif').draw(MAIN_WINDOW)
                    mv_toggle = False

        
    MAIN_WINDOW.close()
    return game_points

# ====== Handles the Movement of the Character ======
# game_chr       : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# direction      : Integer between 0 and 3
# virtual_board         : Virtual game board data
# game_points     : Integer value of the points/score of the game
# dead_wumpus_lst : List containing virtual coordinates of each wumpus, as well as boolean flag for if it's dead or not (True = Dead, False = Alive)
def move_handler(game_chr, direction, virtual_board, game_points, dead_wumpus_lst):
    """Handles movement of the character."""
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

    global MAIN_WINDOW

    virtual_board[game_chr[1]][game_chr[0]][6] = True # Marks the square as having been visited
    # NOTE: This has to be set BEFORE the character is moved so that it doesn't conflict with evaluating the squeare that we're in


    game_chr, bad_move = move_game_character(game_chr, direction, virtual_board)

    # in_sqr is a list that contains all the the items in a given game square. The structure is as follows
    #   [0] - Wumpus : Boolean (true = is in square)
    #   [1] - Gold   : Boolean (true = is in square)
    #   [2] - Pit    : Boolean (true = is in square)
    in_sqr = what_in_square(game_chr, virtual_board)


    ## This sequentially checks if certain items are present in the square, then draws them in the correct order (pit, gold, wumpus).
    ## The game does not undraw anything but the player sprite and the sense string, so board images will tend to accumulate. I'm unaware if that will tend to affect performance.

    if in_sqr[2]:
        Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], virtual_board[game_chr[1]][game_chr[0]][2][1]), 'pit.gif').draw(MAIN_WINDOW)
    if in_sqr[1]:
        Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], virtual_board[game_chr[1]][game_chr[0]][2][1]), 'gold.gif').draw(MAIN_WINDOW)
    if in_sqr[0]:
        Image(Point(virtual_board[game_chr[1]][game_chr[0]][2][0], virtual_board[game_chr[1]][game_chr[0]][2][1]), 'wumpus.gif').draw(MAIN_WINDOW)
    
    game_chr[2].draw(MAIN_WINDOW)

    # Undraws then draws the sense text on the board.
    virtual_board[game_chr[1]][game_chr[0]][7].undraw()
    virtual_board[game_chr[1]][game_chr[0]][7].draw(MAIN_WINDOW)

    ## This evaluates and scores the points
    working_pnts = -1
    
    if bad_move: 
        # Subtracts for invalid move
        working_pnts -= 1 
    
    if in_sqr[2]: 
        # Subtracts for pit
        working_pnts -= 10 
    
    if in_sqr[1] and not virtual_board[game_chr[1]][game_chr[0]][6]: 
        # Adds 100 points for gold
        working_pnts += 100 
    
    for wumpus_count in range(len(dead_wumpus_lst)):
        if dead_wumpus_lst[wumpus_count][2]: # Adds 50 points if the Wumpus is dead and the square hasn't been visited before
            
            if dead_wumpus_lst[wumpus_count][0] == game_chr[0] and dead_wumpus_lst[wumpus_count][1] == game_chr[1] and not virtual_board[game_chr[1]][game_chr[0]][6]:
                working_pnts += 50
                print('found dead wumpus')

    # This checks:
    #   1. If there is a wumpus in the square you walked into.
    #   2. If that wumpus is alive.
    # If both are True, then you've walked in on a live wumpus and you lose 1000 points :(
    if (dead_wumpus_lst[0][0] == game_chr[0] and dead_wumpus_lst[0][1] == game_chr[1] and not dead_wumpus_lst[0][2]) or (dead_wumpus_lst[1][0] == game_chr[0] and dead_wumpus_lst[1][0] == game_chr[1] and not dead_wumpus_lst[1][2]):
        print('hit live wumpus')
        #pprint(dead_wumpus_lst)
        #pprint(game_chr)
        working_pnts -= 1000

    # Sets the official game points to the working copy    
    game_points = game_points+working_pnts
    
    return game_chr, game_points

# ====== Handles the Firing and Scoring of Arrows ======
# game_chr       : List containing virtual X and Y coordinates and Image object ascociated with a "moving object" (player character or arrow)
# direction      : Integer between 0 and 3
# virtual_board         : Virtual game board data
# game_points     : Integer value of the points/score of the game
# dead_wumpus_lst : List containing virtual coordinates of each wumpus, as well as boolean flag for if it's dead or not (True = Dead, False = Alive)
# game_arrow_count : Integer between 0 and 5 with the number of arrows available to the player.
# report_str   : String with the "sound" heard by the player after firing an arrow
def arrow_handler(game_chr, direction, virtual_board, game_points, dead_wumpus_lst, game_arrow_count, report_str):
    """Handles firing and scoring of arrows."""
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
# 4. If you've made a bad_move (e.g. Hit a wall):
#     1. Make a "Thunk" noise
#     2. Stop moving
# 5. Try to move to the next square.
# 6. Repeat 2 - 5 till you stop moving.

    game_arrow = [game_chr[0], game_chr[1], "gameArrow.gif"]
    done_flag = False
    bad_move = False
    report_base = 'Sound:\n-------\n'

    # Initializes the game_arrow variable
    game_arrow[2] = Image(Point(virtual_board[game_arrow[1]][game_arrow[0]][2][0], virtual_board[game_arrow[1]][game_arrow[0]][2][1]), "gameArrow.gif")

    global MAIN_WINDOW
    
    # Creates a list of what's in the current square
    in_sqr = what_in_square(game_chr, virtual_board)

    # Subtract arrows. If you're out of arrows, then you're done.
    if game_arrow_count > 0:
        game_arrow_count -= 1
        game_points -= 5
    else:
        done_flag = True

    # Loop for firing an arrow
    while not done_flag:
        game_arrow[2].undraw()
        game_arrow[2].draw(MAIN_WINDOW)
        time.sleep(0.5)
        print("BadMove:", bad_move)
        #print(game_arrow[0], game_arrow[1])
        
        if bad_move:
            report_str.setText(report_base+"Thunk!")
            done_flag = True
            print("hit a wall")
        elif in_sqr[0]: # If wumpus is in the same square as the arrow

            done_flag = True
            print("Hit a wumpus")
            #pprint(dead_wumpus_lst)
            for wumpus_count in range(len(dead_wumpus_lst)):
                # print(game_arrow[0], dead_wumpus_lst[wumpus_count][0])
                # print(game_arrow[1], dead_wumpus_lst[wumpus_count][1])
                # print(wumpus_count)

                if dead_wumpus_lst[wumpus_count][0] == game_arrow[0] and dead_wumpus_lst[wumpus_count][1] == game_arrow[1]: # Compares current square to list of dead wumpii

                    print(dead_wumpus_lst[wumpus_count][0], dead_wumpus_lst[wumpus_count][1])
                    if dead_wumpus_lst[wumpus_count][2]: # if you hit a dead wumpus
                        report_str.setText(report_base+"Plop!")
                    elif not dead_wumpus_lst[wumpus_count][2]: # If you hit a live wumpus
                        dead_wumpus_lst[wumpus_count][2] = True
                        report_str.setText(report_base+"Scream!")
                        game_points += 500
           
        game_arrow, bad_move = move_game_character(game_arrow, direction, virtual_board, objType=1)
        in_sqr = what_in_square(game_arrow, virtual_board)
        
    game_arrow[2].undraw()
    return game_points, game_arrow_count, report_str



# ====== Prompts the User for their Initials ======
def getInitials():
    """Prompts the user for their initials."""
# Prompts the user for a three letter set of initials (must be 3 letters) that does not contain the @ symbol
    
    done_flag = False

    # Window for entering 
    initials_window = GraphWin("Enter Your Initials", 200, 100)

    # The rectangle that will server as the "done" button
    initial_done_btn = Rectangle(Point(100, 33), Point(150, 66))
    initial_done_btn.draw(initials_window)

    # The entry box for initials
    initials_entry = Entry(Point(70, 50), 3)
    initials_entry.setText("")
    initials_entry.draw(initials_window)

    # Text object that goes in the "done" button
    Text(Point(125, 49), "Done?").draw(initials_window)

    # Loop waits for valid user input
    while not done_flag:
        try:
            my_click = initials_window.getMouse()
        except GraphicsError:
            done_flag = True

        #print(my_click.getX(), my_click.getY())
        if not done_flag:
            is_done_clicked = get_rect_intersect(initial_done_btn, my_click)
            if is_done_clicked:
                initials_text = initials_entry.getText()
                if len(initials_text) == 3 and "@" not in initials_text:
                    done_flag = True
                    initials_window.close()
    
    return initials_text

# +++++++ Handler for Game Score and High Score File ++++++
def gameHandler():
    """Handler for the game score and high score file."""
# Takes the score from the game played by the user
# Reads the existing high scores from file
# If the entered initials are the highest score for that set of initials OR the initials are not yet represented in the high score file, then the high score data is added
# Takes the list of high scores and orders them based on score
# Displays a window that shows the list of top 10 scores
# Writes all scores to file (overwriting the old file)
    
    game_score = main() # Gamescore retrieved from Main
    global GAMEDIFF # Accesses gamediff

    score_window = GraphWin("High Scores!", 400, 400)

    initials_text = getInitials().upper() # Gets the entered initials from the user.
    print(initials_text)
    
    # NOTE: This file needs to be created.
    high_scores_file_name = "lfbWumpusHighScores.txt"
    

    high_scores_file = open(high_scores_file_name, 'r')

    eof = False # Used to flag the end of a file.
    #print('got to open file')
    # The structure of the highscores file is as follows:
    # Each line contaings the following data:
    #   0 - High score (integer)
    #   1 - Game Difficulty (integer)
    #   2 - Initials (string)
    # Each of these values will occur on each line in that order, delimited by the "@" symbol
    print("")
    score_list = []
    while not eof:
        text_line = high_scores_file.readline()
        print('txtLine', text_line)
        if len(text_line) > 0:
            print("txtLine", text_line)
            score_list.append((text_line.strip()).split('@')) # Strips the newline and splits on the @

        else: eof = True

    eof = False

    high_scores_file.close() # Closes the file to avoid later conflict
    #pprint(score_list)
    score_list_working_copy = score_list # Working copy of score_list
    append_flag = True # Flag for appending new score

    for entry in score_list_working_copy:
        score_list[score_list_working_copy.index(entry)][0] = eval(entry[0])
        score_list[score_list_working_copy.index(entry)][1] = eval(entry[1])

    score_list_working_copy = score_list # Resets as working copy again

    # This loop ensures one entry per set of initials, and that that entry is the largest of all the ones entered.
    for entry in score_list_working_copy:
        if initials_text == entry[2]:
            if game_score >= entry[0]:
                del score_list[score_list.index(entry)] # If the initials exist and are asscociated with a lower score, delete them from the list
            elif game_score < entry[0]: # If the same initails are assciciated with a higher score, then don't display the given score
                append_flag = False

    if append_flag:
        score_list.append([game_score, GAMEDIFF, initials_text])

    # Creates top_list as working copy of score_list
    top_list = sorted(score_list, reverse=True) # Automatically sorts by score, from highest to lowest
    top_list = top_list[0:10] # Limits the score_list to the top 10 scores

    # Will be the string that shows the nice scores
    print_scores = "|  Score  | Difficulty | Initials |\n"

    for stuff in top_list:
        if stuff[2] == 0:
            # Note a flagrant bug here: I get a diff_string, then I never use
            # it again. Instead, the number representing the difficulty is
            # used. So instead of saying "easy", "medium", "hard" it says "0",
            # "1", "2".
            diff_string = "Easy"
        elif stuff[2] == 1:
            diff_string = "Medium"
        elif stuff[2] == 2:
            diff_string = "Hard"
        print_scores += "{0:^10}{1:^14}{2:^7}\n".format(stuff[0], stuff[1], stuff[2])

    print(print_scores)
    print_scores = Text(Point(200, 200), print_scores)
    print_scores.setFace('courier')
    print_scores.setSize(12)
    print_scores.draw(score_window)

    high_scores_file = open(high_scores_file_name, 'w')
    score_list_working_copy = "" # Reassignment for compaction

    for stuff in score_list:
        score_list_working_copy += str(stuff[0])+'@'+str(stuff[1])+'@'+str(stuff[2])+'\n'

    high_scores_file.write(score_list_working_copy)

    # All this is doing is waiting for the user to manually close the high-
    # score list window. It's super ghetto, and I don't know why it's done
    # this way.
    while not eof:
        try:
            my_click = score_window.getMouse()
        except: eof = True
    score_window.close()

gameHandler()

#btnSize()
