from visual import *
from robot import *
from random import *
import time 

GROUNDRADIUS = 100
def main():
    playerHealth = 20 #set health of the player(s)
    ground = cylinder(pos=(0,-100,0),axis = (0,100,0),radius = GROUNDRADIUS)
    numplayers = 2 #sets number of players
    userbot = r2d2(health = playerHealth) #initializes the players robot, r2d2
    numBots = 10 #number of enemies
    botList = [] #list to store info about the enemies
    botHealth = 2 #set health of the enemies 
    laserList = [] #list to keep track of info about the lasers
    manuel = False # boolean to set manuel control status
    if numBots > 0: 
        counter = numBots #counter will keep track of how many bots are left- key to "winning" this game mode
    else:
        counter = 1 # prevents win message from triggering if mode is only p1 vs p2
    if numplayers ==2: #initalize the second player if mode is 2 player or pvp 
        start = vector(0,0,20)
        userbot2 = r2d2(position=start,health = playerHealth)
        userbot2.head.color = color.red
        userbot2.leg1.color=color.red
        userbot2.leg2.color=color.red
    for number in range(numBots): #initialize the enemy robots 
        posx = randint(0,60)
        posz = randint(0,60)
        randpos = vector(posx,0,posz)
        bot = ranbot(position = randpos,health=botHealth) # set the health of each enemy robot 
        botList.append(bot) #add to botList, where the bots actions will be taken care of 
    fired = False

    while counter!=0:
        rate(30)  # 30 frames per second
        if scene.kb.keys: # is there an event waiting to be processed?
            s = scene.kb.getkey() # obtain keyboard information
            ###PLAYER 1 CONTROLS
            if s == "w":          # if the user pressed the w...  
                userbot.forward(userbot.speed)   # ... go forward
            elif s == "a":
                userbot.backward(userbot.speed)
            elif s == "s":
                userbot.turn(20)
            elif s == "d":
                userbot.turn(-20)
            elif s == '1':
                userbot.speed += 0.1
            elif s == '2':
                userbot.speed -= 0.1
            elif s == 'q':
                    ls = laser(userbot.base,userbot.heading) # create a laser object
                    ls.body.color = color.blue
                    laserList.append(ls) #add it to the list so it can be kept track of 
                    fired = True
            elif s ==' ':
                userbot.jump()
            elif s=='m': #toggle manuel movement 
                if manuel == True:
                    manuel = False
                elif manuel == False:
                    manuel = True
            ## PLAYER 2 CONTROLS 
            elif s == 'p':
                ls = laser(userbot2.base,userbot2.heading) #create a laser object
                ls.body.color = color.green
                laserList.append(ls) #add it to the list so it can be kept track of 
                fired = True 
            elif s == 'o':
                userbot2.forward(userbot2.speed)
            elif s == 'l':
                userbot2.backward(userbot2.speed)
            elif s == 'j':
                userbot2.turn(20)
            elif s == 'k':
                userbot2.turn(-20)
            elif s == '9':
                userbot2.speed += 0.1
            elif s == '0':
                userbot2.speed -= 0.1
            else:
                pass # do nothing

                
        # Userbot rules
        if manuel == False: # if manuel mode is off
            userbot.forward(userbot.speed) #robot will move automatically
            if numplayers>1: # same goes for player 2 
                userbot2.forward(userbot2.speed)
        if mag(userbot.base) >= GROUNDRADIUS: 
            userbot.turn(180) # if hit edge, turn around
        if numplayers > 1 and mag(userbot2.base) >= GROUNDRADIUS: 
            userbot2.turn(180) # same for player 2 


        # Update ranbots
        if len(botList)!=0:
            for number in range(numBots): #go through list of enemy robots
                bot = botList[number]
                bot.forward(bot.speed) # move bot forward
                num = randint(0,500) # choose random num to simulate random motion
                if num > 250:  # if less than 5 turn right
                    bot.turn(5)
                    if num >490 and bot.body.visible == True :
                        ls = laser(bot.base,bot.heading) # create a laser object
                        ls.body.color = color.red
                        laserList.append(ls) #add it to the list so it can be kept track of 
                        fired = True
                else: bot.turn(-5) # else turn left
                if mag(bot.base) >= GROUNDRADIUS: bot.turn(180) #if at edge, turn around
                if (bot.intersectTest(userbot.base)==True or userbot.intersectTest(bot.base)==True) and bot.body.visible==True: # if user runs into an enemy robot, they get damaged
                    userbot.health -= 1 # decrease player 1's health
                    userbot.flashRed() #flash red to show damage
                    if userbot.health ==0: #if health is 0 
                        userbot.delete() #delete player 1
                if numplayers !=1:
                    if (bot.intersectTest(userbot2.base)==True or userbot2.intersectTest(bot.base)==True) and bot.body.visible == True: # if user 2 runs into an enemy robot, they get damaged
                        userbot2.health -= 1 # decrease player 2's health
                        userbot2.flashRed() #flash red to show damage
                        if userbot2.health ==0: #if health is 0 
                            userbot2.delete() #delete player 2
                    if userbot.body.visible == False and userbot2.body.visible == False: # if both players die, game over, robots win
                        losemessage = text(text="Both players have been destroyed by Ran-Troopers",align='center',height = 400,depth=-0.2, color=color.red) 
        # handling the lasers
        #laser status - are lasers being fired?
        if len(laserList) == 0:
                    fired = False
        #dealing with moving the lasers and deciding if they are hitting anything, and what should happen if they are 
        if fired ==True: 
            for i in range(len(laserList)): #laser list has all the lasers that have been fired 
                shot = laserList[i] ## get laser  
                shot.forward(shot.speed) # move the laser forward
                for number in range(numBots): #check to see if the laser is hitting any enemy bots
                    bot = botList[number] 
                    if bot.intersectTest(shot.base)==True or shot.intersectTest(bot.base)==True: # if the laser is hitting the bot
                        bot.health -= 1 #decrease it's health by 1 
                        bot.flashRed() #flash red to show damage
                        shot.delete()
                        if bot.health ==0: # if the bots health has been reduced to 0
                            bot.delete() #delete the bot
                            del bot
                            counter -= 1 #decrement the counter
                if numplayers > 1:  # if there is a second player, check to see if the laser is hitting that player
                    if userbot2.intersectTest(shot.base)==True or shot.intersectTest(userbot2.base)==True: # if the laser is hitting player 2
                        userbot2.health -= 1 # decrease player 2's health
                        userbot2.flashRed() #flash red to show damage
                        if userbot2.health ==0: #if health is 0 
                            userbot2.delete() #delete player 2
                            winText = text(text = "Player 1 destroyed Player 2",align='center',height = 400,depth=-0.3, color=color.blue) # show that player 1 won 
                if userbot.intersectTest(shot.base)==True or shot.intersectTest(userbot.base)==True: # if the laser is hitting player 1
                    userbot.health -= 1 # decrease player 1's health
                    userbot.flashRed() #flash red to show damage
                    if userbot.health ==0: #if health is 0 
                        userbot.delete() #delete player 1
                        winText = text(text = "Player 2 destroyed Player 1",align='center',height = 400,depth=-0.3, color=color.red) # show that player 2 won 
                if mag(shot.base) >= GROUNDRADIUS: #if the laser hits the edge, it goes away
                    shot.delete() #delete the shot
            # laser list dump
            v = 0 
            for i in range(len(laserList)):
                shot = laserList[i]
                if shot.body.visible == False:
                    v+=1
            if v == len(laserList):
                laserList = []
            print len(laserList)

    winText = text(text = "Players have destroyed the Ran-Troopers",align='center',height = 400,depth=-0.3, color=color.blue) # win promt for the 1 player/ ranbot's exist mode 
        
if __name__ == "__main__" : main()
