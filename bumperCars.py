# bumperCars.py
#
# Author:     Chi Nguyen
# Email:      nguyenct1@g.cofc.edu
# Class:      CITA 284 
# Assignment: Homework #7
# Due Date:   15 April 2024
#
# Purpose: Cars will bounce off each other and display boundaries and
#          produce sound effects. Singleplayer mode has NPCs (Non
#          Playable Cars), while multiplayer has other players, with
#          the option of NPCs. Players control their car with their
#          phones using TouchOSC. Multiplayer option allows players to
#          choose their car color. Took inspiration from Boids.
#
# Input:   TouchOSC data
#
# Output:  A bumper car simulator
# Notes:   chasing, osc objects for player ports, 

from gui import *
from math import *
from random import *
from osc import *
from music import *

#SCHOOL 10.5.194.53

# game audios
carnival = AudioSample("\oscBumper\carnival.wav")
carnival.loop(times = -1, start = 0, size = -1, voice = 0)
carBonk = AudioSample("oscBumper\carBonk.wav")
playerBonk = AudioSample("\oscBumper\playerBonk.wav")
platformBonk = AudioSample("\oscBumper\platform.wav")

# platform parameters
platformWidth  = 500      # how wide the display, 1260 preferred
platformHeight = 680       # how high the display, 675 preferred
  
# generation parameters
numNPCs     = 6            # number of NPC
numPlayer   = 1            # number of Players
carRadius   = 20           # radius of cars
playerColor = Color.ORANGE # default is blue
npcColor    = Color.BLACK  # default is black
  
# car distance parameters
minSeparation = carRadius * 2 # min comfortable distance between two cars
carThreshold  = 1             # cars closer than this are grouped
  
# NPC behavior parameters
separationFactor = 0.001   # how quickly they separate
alignmentFactor  = 0.05    # aligning with other NPCs
cohesionFactor   = 0.005   # moving to attraction point
frictionFactor   = 1.1     # friction

# OSC set up
oscIn = OscIn(28825)
arg1 = 0
arg2 = 0

# currently moving all cars, need a separate
# move function for Player, oopsie
def movePlayerCar(message):
   global platform, arg1, arg2, outputArray
   
   address = message.getAddress()
   args = message.getArguments()
   output = str(args)
   outputArray = output.split(",")

   # Check if outputArray has at least 2 arguments
   if len(outputArray) >= 3:
      arrayMsg = outputArray[0]
      # stripping the strings to only numbers
      arg1 = float(outputArray[1].replace("[", "").replace("]", "").replace(")", "").strip())
      arg2 = float(outputArray[2].replace("[", "").replace("]", "").replace(")", "").strip())
      # test prints
      print arg1, arg2
        
      # mapping values and updating Player's attraction point
      carX = arg1
      carY = arg2 
      platform.playerPoint = complex(carX, carY)

# function call
oscIn.onInput("/28825", movePlayerCar)

# the Platform where the game takes place
class BumperPlatform:
   
   def __init__(self, title = "", width = 600, height = 600, frameRate=30):
      
      # platform display
      self.display = Display(title, width, height, 0, 0, Color(100, 0, 0))
      self.rect = Rectangle(75, 75, width - 75, height - 75, Color(255, 100, 100, 150), True, 50)
      self.horizLine1 = Line(0, int(height * 0.25), width, int(height * 0.25), Color.BLACK, 1)
      self.horizLine2 = Line(0, int(height * 0.50), width, int(height * 0.50), Color.BLACK, 1)
      self.horizLine3 = Line(0, int(height * 0.75), width, int(height * 0.75), Color.BLACK, 1)
      self.vertiLine1 = Line(int(width * 0.25), 0, int(width * 0.25), height, Color.BLACK, 1)
      self.vertiLine2 = Line(int(width * 0.50), 0, int(width * 0.50), height, Color.BLACK, 1)
      self.vertiLine3 = Line(int(width * 0.75), 0, int(width * 0.75), height, Color.BLACK, 1)
      
      self.display.add(self.rect)
      self.display.add(self.horizLine1)
      self.display.add(self.horizLine2)
      self.display.add(self.horizLine3)
      self.display.add(self.vertiLine1)
      self.display.add(self.vertiLine2)
      self.display.add(self.vertiLine3)
      
      # list of NPCs and Players
      self.npcs = []
      self.players = [] 
  
      # attraction point for NPCs (initially, platform center)
      self.attractPoint = complex(width/2, height/2)  
  
      # attraction point for Players (initially, platform center)
      self.playerPoint = complex(width/2, height/2)
      
      # game timer
      delay = 1000 / frameRate    
      self.timer = Timer(int(delay), self.animate)
  
      # mouse testing for OSC implementation
      self.display.onMouseDrag(self.moveAttractionPoint)
      
   def start(self):
      self.timer.start()  
  
   def stop(self):
      self.timer.stop()
  
   def addNPC(self, npcs):
      self.npcs.append(npcs)          # adding NPC to array
      self.display.add(npcs.circle)   # creating the NPC
      self.display.add(npcs.icon)    
      
   def addPlayer(self, players):
      self.players.append(players)     # adding Player to array
      self.display.add(players.circle) # creating the Player
      self.display.add(players.icon)
  
   def animate(self):
      # sensing and acting for all cars
      for npc in self.npcs:
         npc.sense(self.npcs, self.players, self.attractPoint) 
         npc.act(self.display)   
          
      for player in self.players:
         player.sense(self.players, self.npcs, self.playerPoint)
         player.act(self.display)   
                
   def moveAttractionPoint(self, x, y):
      # moves NPCs attraction point
      self.attractPoint = complex(x, y)
   
   def movePlayer(self, x, y):
      # moves Player attraction point
      self.playerPosition = complex(x, y)

class NPC:
   global carBonk, platformBonk # audio file
   def __init__(self, x, y, radius, color, initVelocityX=1, initVelocityY=1):

   # filled circle base, color customizable in multiplayer
      self.circle = Circle(x, y, radius, color, True) 

   # car icon
      iconSize  = int(carRadius * 1.5)
      self.icon = Icon("carIcon.png", iconSize)

   # set car size and position
      self.radius = radius                # car radius
      self.coordinates = complex(x, y)    # car coordinates (x, y)

   # car velocity (x, y)
      self.velocity = complex(initVelocityX, initVelocityY)  
   
   #inspired by boids
   def sense(self, players, npcs, center):
  
      # 1. Rule of Separation - move away from other cars
      self.separation_players = self.rule1_Separation(players)
      self.separation_npcs = self.rule1_Separation(npcs)
  
      # 2. Rule of Alignment - aligning with other cars
      self.alignment_players = self.rule2_Alignment(players)
      self.alignment_npcs = self.rule2_Alignment(npcs)
  
      # 3. Rule of Cohesion - move toward the center of the Platform
      self.cohesion = self.rule3_Cohesion(npcs, center)
      
      # interaction with Players and NPCs - move away from both to avoid collisions
      for player in players:
         if self.distance(player) < minSeparation:
            self.velocity -= (player.coordinates - self.coordinates)
      for npc in npcs:
         if self.distance(npc) < minSeparation:
            self.velocity -= (npc.coordinates - self.coordinates)
                
      # composite behavior
      self.velocity = ((self.velocity / frictionFactor) + \
                      self.separation_players + self.separation_npcs + \
                      self.alignment_players + self.alignment_npcs + \
                      self.cohesion) 
  
   def act(self, display):
      # update coordinates
      self.coordinates = self.coordinates + self.velocity
      x = self.coordinates.real
      y = self.coordinates.imag
      
      # bounces back if cars hit the border
      if x < self.radius:
         x = self.radius
         self.velocity = complex(-self.velocity.real, self.velocity.imag) 
         #platformBonk.play()
      elif x > platformWidth - self.radius:
         x = platformWidth - self.radius
         self.velocity = complex(-self.velocity.real, self.velocity.imag)
         #platformBonk.play()
      if y < self.radius:
         y = self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag) 
         #platformBonk.play()
      elif y > platformHeight - self.radius:
         y = platformHeight - self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag)
         #platformBonk.play()
      
      iconCenterX = self.radius * 0.72
      iconCenterY = self.radius * 0.8
   
      # act 
      display.move(self.icon, int(x - iconCenterX), int(y - iconCenterY))
      display.move(self.circle, int(x), int(y))
  
   # defining rules
   def rule1_Separation(self, npcs):
      # holds new velocity
      newVelocity = complex(0, 0) 
      
      for npc in npcs:
         separation = self.distance(npc)
         # checks if too close to other cars
         if separation < minSeparation and npc != self:
            newVelocity = newVelocity - (npc.coordinates - self.coordinates)
            #carBonk.play()  
      # return new velocity      
      return newVelocity * separationFactor  
  
   def rule2_Alignment(self, npcs):
      # holds sum of car velocities
      totalVelocity = complex(0, 0) 
      # count of local cars
      numLocalCars = 0       
   
      for npc in npcs:
         # get car distance
         separation = self.distance(npc)
         # if this a local car, record its velocity
         if separation < carThreshold and npc != self:                      
            totalVelocity = totalVelocity + npc.velocity             
            numLocalCars = numLocalCars + 1     
           
      # average car      
      if numLocalCars > 0:
         avgVelocity = totalVelocity / numLocalCars
      else:
         avgVelocity = totalVelocity
   
      newVelocity = avgVelocity - self.velocity
   
      # return new velocity
      return newVelocity * alignmentFactor  
  
   def rule3_Cohesion(self, npcs, center):
      # return new velocity
      newVelocity = center - self.coordinates
      return newVelocity * cohesionFactor 
  
   # Euclidean distance calculating function
   def distance(self, other):

      xDistance = (self.coordinates.real - other.coordinates.real)
      yDistance = (self.coordinates.imag - other.coordinates.imag)
  
      return sqrt(xDistance*xDistance + yDistance*yDistance)

class Player:
   global playerBonk, platformBonk # audio file
   def __init__(self, x, y, radius, color, initScore=0, initVelocityX=1, initVelocityY=1):

   # filled circle base, color customizable in multiplayer
      self.circle = Circle(x, y, radius, color, True) 

   # car icon
      iconSize  = int(carRadius * 1.5)
      self.icon = Icon("carIcon.png", iconSize)

   # set car size and position
      self.radius = radius                # car radius
      self.coordinates = complex(x, y)    # car coordinates (x, y)
   
   # player port and score ####################
      
      self.score = initScore
      self.scoreTag = Label(str(self.score))
      self.scoreTimer = Timer(1000, self.addScore)
      self.scoreTimer.start()
      

   # car velocity (x, y)
      self.velocity = complex(initVelocityX, initVelocityY)  

   # attraction point for Players (initially, Platform center)
      self.playerPoint = complex(platformWidth/2, platformHeight/2) #method####################

   def movePlayer(self, x, y):
      # moves Player attraction point
      self.playerPoint = complex(x, y)
      
   def addScore(self):
      self.score += 5
      self.scoreTag = str(self.score)  # Update displayed score
  
   # inspired by boids
   def sense(self, players, npcs, center):
      
      # 1. Rule of Separation - move away from other cars
      self.separation_players = self.rule1_Separation(players)
      self.separation_npcs = self.rule1_Separation(npcs)
  
      # 2. Rule of Alignment - aligning with other cars
      self.alignment_players = self.rule2_Alignment(players)
      self.alignment_npcs = self.rule2_Alignment(npcs)
  
      # 3. Rule of Cohesion - move toward the center of the Platform
      self.cohesion = self.rule3_Cohesion(players, center)
  
      # interaction with Players and NPCs - move away from both to avoid collisions
      for player in players:
         if self.distance(player) < minSeparation:
            self.velocity -= (player.coordinates - self.coordinates)
      for npc in npcs:
         if self.distance(npc) < minSeparation:
            self.velocity -= (npc.coordinates - self.coordinates)
                
      # composite behavior
      self.velocity = ((self.velocity / frictionFactor) + \
                      self.separation_players + self.separation_npcs + \
                      self.alignment_players + self.alignment_npcs + \
                      self.cohesion)
  
   def act(self, display):
      # update coordinates
      self.coordinates = self.coordinates + self.velocity
      x = self.coordinates.real
      y = self.coordinates.imag
      
      # bounces back if cars hit the border
      if x < self.radius or x > platformWidth - self.radius \
                or y < self.radius or y > platformHeight - self.radius:
            self.velocity = -self.velocity  # Reverse velocity
            self.score -= 1  # Decrement score when hitting the border
         #platformBonk.play()
         
      iconCenterX = self.radius * 0.72
      iconCenterY = self.radius * 0.8

      # act
      display.move(self.icon, int(x - iconCenterX), int(y - iconCenterY))
      display.move(self.circle, int(x), int(y))
      #display.move(self.scoreTag, int(x), int(y))
  
   # defining rules
   def rule1_Separation(self, players):
      # holds new velocity
      newVelocity = complex(0, 0)  
      
      for player in players:    
         separation = self.distance(player)
         # checks if too close to other players
         if separation < minSeparation and player != self:
            newVelocity = newVelocity - (player.coordinates - self.coordinates)
            self.score -= 1
            print(self.score)
            #playerBonk.play() 
      # return new velocity
      return newVelocity * separationFactor
  
   def rule2_Alignment(self, players):
      # holds sum of car velocities
      totalVelocity = complex(0, 0) 
      # count of local cars
      numLocalCars = 0  

      for player in players:
         # get car distance
         separation = self.distance(player)    
         # if this a local car, record its velocity
         if separation < carThreshold and player != self:                      
            totalVelocity = totalVelocity + player.velocity             
            numLocalCars = numLocalCars + 1     
           
      # average car velocity     
      if numLocalCars > 0:
         avgVelocity = totalVelocity / numLocalCars
      else:
         avgVelocity = totalVelocity
   
      newVelocity = avgVelocity - self.velocity
      
      # return new velocity
      return newVelocity * alignmentFactor  
  
   def rule3_Cohesion(self, players, center):
      # return new velocity
      newVelocity = center - self.coordinates
      return newVelocity * cohesionFactor
  
   # Euclidean distance calculating function
   def distance(self, other):
  
      xDistance = (self.coordinates.real - other.coordinates.real)
      yDistance = (self.coordinates.imag - other.coordinates.imag)
  
      return sqrt(xDistance*xDistance + yDistance*yDistance)

# start car simulation
platform = BumperPlatform(title="Bump Itz", width=platformWidth, height=platformHeight)

# create Player
for i in range(0, numPlayer):
  
   # get random position for this car
   x = randint(0, platformWidth)
   y = randint(0, platformHeight)
  
   # create a car with these parameters
   player = Player(x, y, carRadius, playerColor, 0, 1, 1)
   print(player.score)
   platform.addPlayer(player)

# create NPCs
for i in range(0, numNPCs):
  
   # get random position for this car
   x = randint(0, platformWidth)
   y = randint(0, platformHeight)
  
   # create a car with random position and velocity
   npc = NPC(x, y, carRadius, npcColor, 0.25, 0.25)
   platform.addNPC(npc)
   
#animate cars
platform.start()