# Robot-Game
vPython robot game created for CS5: Intro to CS/Bio course
Note that this project uses the vPython 3D graphics package: http://vpython.org

R2 Droids Versus the Ran-Troopers
by Wyatt Cooper

Part I: Objective
The objective can be customized in various ways.  The default mode is 2 player with 3 Ran-Troopers.  Both players can destroy the enemy Ran-Troopers or destroy each other.  The players will be damaged by each others lasers, by colliding with Ran-Troopers, and by being shot at by the Ran-Troopers.  The Ran-Troopers move and shoot lasers at random.  
If the number of bots is set to 0, the game because a battle between Player 1 and Player 2.  

Part II: Controls

PLAYER 1 CONTROLS:
q - fire laser.  Note that laser firing is extremely spammable, and at first this is fine.  The way the game handles the laser objects is very memory-wasteful, so after many lasers have been fired, it gets a little laggy.  However for the purposes of the objective, and as long as there aren't too many enemy Ran-Troopers, it is generally fine.  
s - turn right
d - turn left
1 - speed up
2 - slow down
spacebar - jump.  This feature is rather useless and does not serve any role in the gameplay.  It looks kind of cool, and it is just for player 1. 
m - toggles manuel forward/backward movement.  If manuel movement is toggled:
	w - forward
	a - backwards

PLAYER 2 CONTROLS:
p - fire laser.  Same as above.  
j - turn right
k - turn left 
9 - speed up
0- slow down
m - toggles manuel movement.  If manuel movement is toggled:
	o - forward
	l - backwards

CUSTOMIZABLE FEATURES:
There are a few attributes in the game that can be easily customized.  
Player health - default set to 10 for both Player 1 and Player 2
Ran-Trooper health - default set to 2
Number of players - max of 2
Number of enemy Ran-Troopers - default at 2, max of theoretically a lot, but it is not recommended to make a lot (you'll probably lose/crash your computer)
Ground radius - the ground radius can also be adjusted

Additional features are the intersection testing, which compares two vectors and decides if one vector in within a certain range of another.  This is essential for the handling of lasers and the collisions between characters.  Another features, in which characters will "flash" when damaged, was made possible with the time package from Python, in which sleep(0.5) was used to seperate two for loops that changed the color of the robot.  
