from visual import *
import math
import time

class robot:
    def __init__(self, position=vector(0,0,0), heading=vector(0,0,1),health=1):
        self.health = health
        self.base = vector(position)
        self.heading = vector(norm(heading))
        self.parts = []

    def forward(self, amount):
        self.base += self.heading * amount
        for part in self.parts:
            part.pos += self.heading * amount
    def backward(self, amount):
        self.base -= self.heading * amount
        for part in self.parts:
            part.pos -= self.heading * amount

    def turn(self, angle):
        theta = math.radians(angle)
        self.heading = rotate(self.heading, angle=theta, axis=(0, 1, 0))
        for part in self.parts:
            part.rotate(angle=theta, axis=(0,1,0), origin=self.base)

    def jump(self):
        '''Jump up and fall back down.'''
        ## jumping up
        jumpAmount = vector(0,10,0)
        vel = vector(0,-5,0)
        self.base += jumpAmount
        for part in self.parts:
            part.pos += jumpAmount
        ## falling back down 
        ## taken from bounce example
        RATE = 15
        dt = 1.0/RATE
        while vel.y != 0.0:
            rate(RATE)
            for part in self.parts:
                part.pos = part.pos + vel*dt
                if part.pos.y < 0: 
                  vel.y = 0.0
        self.base -= jumpAmount
    def delete(self):
        '''deletes the robot from the map by making all of its parts invisible and then deleting them.  Unclear if del actually deletes the part from the map'''
        for part in self.parts:
            part.visible = False
            del part ##not sure if this does what it is supposed to 

    def intersectTest(self,Vector):
        '''Decides if a vector Vector is colliding with any parts of the robot self'''
        newVector = vector(0,0,0) # need to make a new vector variable to store the info of the vector we want to test in the intersection
        # so that the attributes don't get changed 
        newVector.x = Vector.x
        newVector.y = Vector.y
        newVector.z = Vector.z
        newVector = vector(newVector.x,newVector.y,newVector.z) # info transfered to new variable 
        for part in self.parts: # test all the parts for intersections 
            r = 2.2 # r measures the range to qualify for intersection 
            # variables to bound the ranges
            upperX = int(part.pos.x) + r
            lowerX = int(part.pos.x) - r
            upperY = int(part.pos.y) + r
            lowerY = int(part.pos.y) - r
            upperZ = int(part.pos.z) + r
            lowerZ = int(part.pos.z) - r 
            # booleans to test if Vector (with info stored in newVector) is in the ranges
            InX = (newVector.x <= upperX and newVector.x>=lowerX)
            InY = (newVector.y <= upperY and newVector.y>=lowerY)
            InZ = (newVector.z <= upperZ and newVector.z>=lowerZ)
            if InX and InY and InZ: # if the vector is within the range of collision, return true
                return True
                print True

    def flashRed(self):
        '''robot will flash red'''
        oldcolorList = {}
        for part in self.parts:
            oldcolorList[part]= part.color # dictionary to store the old colors 
        for part in self.parts:
            part.color = color.red
        sleep(0.125) #everything stops and waits for 5 seconds
        for part in self.parts:
            part.color = oldcolorList[part] # repaint everything as old colors


class ranbot(robot):
    def __init__(self, position=vector(0,0,0), heading=vector(0,0,1), speed=0.3,health=1):
        robot.__init__(self, position, heading,health)
        self.body = cylinder(pos = self.base+vector(0, 0.5, 0), axis=(0, 6, 0), radius=1, color=color.white)
        self.head = box(pos= vector(0,7,0)+self.base, length = 2, width = 2, height = 2, color=color.black)
        self.nose = cone(pos = vector(0,7,1)+self.base, radius = 0.5, axis=(0,0,1), color=color.white)
        self.wheel1 = cylinder(pos = self.base + vector(1, 1, 0), axis=(0.5, 0, 0), radius = 1, color=color.black)
        self.wheel2 = cylinder(pos = self.base + vector(-1, 1, 0), axis=(-0.5, 0, 0), radius = 1, color=color.black)
        self.arm1 = cylinder(pos = self.base + vector(1, 4.5, 0), axis=(1.5, 0, 0), radius = 1, color=color.black)
        self.arm2 = cylinder(pos = self.base + vector(-1, 4.5, 0), axis=(-1.5, 0, 0), radius = 1, color=color.black)
        self.parts = [self.body, self.head, self.nose, self.wheel1, self.wheel2,self.arm1,self.arm2]
        self.speed = speed
class r2d2(robot):
    def __init__(self,position=vector(70,0,0),heading=vector(0,0,1),speed=0.8,health=1):
        robot.__init__(self,position,heading,health)
        self.body = cylinder(pos = self.base+vector(0, 0.5, 0), axis=(0, 3, 0), radius=1, color=color.white)
        self.head = sphere(pos=vector(0,4,0)+self.base,radius=1,color = color.blue)
        self.leg1= box(pos=self.base+vector(1,1,0), axis = (0.5,0,0),length=0.5,color=color.blue)
        self.leg2= box(pos=self.base+vector(-1,1,0), axis = (0.5,0,0),length=0.5,color=color.blue)
        self.parts = [self.body, self.head, self.leg1, self.leg2]
        self.speed = speed
class laser(robot):
    def __init__(self,position=vector(0,0,0),heading=vector(0,0,1),speed=15.0,health=1):
        robot.__init__(self,position,heading,health)
        self.body = cylinder(pos = self.base+vector(0, 0.5, 0), axis=6*heading, radius=0.2, color=color.red)
        self.parts = [self.body]
        self.speed = speed
