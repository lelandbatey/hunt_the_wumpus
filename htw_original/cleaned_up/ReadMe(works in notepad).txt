ReadMe.txt(OPEN ME IN NOTEPAD++)


Leland Batey

CPTS 111

WSU-TriCities

Hunt the Wumpus - Final Project



Gameplay Notes:

==============

	The user interface for shooting and moving is combined. There are two buttons below the four arrows: "Move" and "Shoot". These are your different modes. Whichever button is blue is the one that is "engaged." To change your operating mode, click the button that is disengaged. For example:

		The game starts in "Move" mode, with the "Move" button being blue and the "Shoot" button being white. To switch to "Shoot" mode, click on the "Shoot" button. This will cause the "Shoot" button to becom blue, and the "Move" button to become white.

	Be aware that potentially, a Pit, Gold, and Wumpus could be in the same square. There will never be multiple of any single type of game object in any square, but there may be different types in the same square.

	Once you've finished playing, you can exit *only the main game window* by pressing the red "X" button in the top right corner of the window. The game will handle that kind of exit from that window. However, doing so on any other window may have adverse consequences.



Assumptions

===========

	1. If the user closes the "Choose Difficulty" window, the game will not be played (though the game window will briefly flash open). However, the default score of 100 points will still be created and the game will ask for your initials and add your score to the high score file.

	2. In every case, closing a window via the red "X" button will not trigger the defualt error. However, it may cause other areas of the program to break. It is pretty much interpretted as a very hard "GET ME OUT OF HERE" action.


Things That are Slightly Odd

============================

	1. The game character will always have a tendency to start in the lower right-hand corner of the game board.

	2. High scores are recorded to a file that must already exist. I'm slightly unsure if this is in the requirements, but the file containing high scores will not be created by the program, so it must already exist.

	3. All (unique) initials/scores are appended to the high scores file. However, the game will only show the top 10. This does violate SRS 5.4.2b, but I believe you had stated that as long as we made note of minor changes such as this, then we could keep them in our program. Given that the user experience is no different than had I followed the requirements, I believe that this change should be allowed to stand.

	4. There is no distinction between different difficulty levels in the high score file. Thus, if you score 1000 points on Hard, but someone else scores 1200 points on Easy, they will have the higher score.

	5. The arrow is visible when it's shot. However, it stops when it hits something. This means that if the arrow hits a wumpus, you will be able to tell which square it is in (potentially making the game easier). Note that this is not an *explicit* discovery, but it could be interpreted as an implicit discovery. However, for style reasons I left it in the game.

	6. If you are in a square with a pit/live wumpus AND the square you are in is right next to a wall, and you try to move into the wall, the game will not only subtract points for trying to move and for bumping into the wall, the game will also act as though you just moved into that square from another square. This means though you didn't "leave," you will recieve the point deductions from the pit/wumpus.




Other Project Notes:

====================

	Even though we were not allowed to use object oriented programming, I found that I trended towards a kind of "proto-OOP" style where I started using common structures for data, then creating more generic functions to manipulate those common data structures. I found this to be a very helpful trend, which makes programming a lot easier.



Attribution:

------------

The image for the game character was originally made for the game Final Fantasy by SquareSoft. The image was reproduced from the game by the Deviantart.com user Ryker.

The image for the floor tile was created as part of the Sphax texture pack for the game Minecraft by the Minecraft user Sphax.

Functions gRectIntersect and xyListCreate were written by Russel Swannack as part of his CPTS 111 course at Washington State University: Tri-Cities. Used with permission.