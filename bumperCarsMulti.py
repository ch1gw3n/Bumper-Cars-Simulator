# bumperCarsMulti.py
#
# Author:     Chi Nguyen
# Email:      nguyenct1@g.cofc.edu
# Class:      CITA 284 
# Assignment: Final Project
# Due Date:   26 April 2024
#
# Purpose: Cars will bounce off each other and display boundaries and
#          produce sound effects. Singleplayer mode has NPCs (Non
#          Playable Cars), while multiplayer has other players, wit
#          the option of NPCs. Players control their car with interface.py
#          code. Multiplayer option allows players to choose their car color. 
#          Took inspiration from Boids.
#
# Input:   OSC data from interface.py code

from gui import *
from math import *
from random import *
from osc import *
from music import *

# game audios
carBonk = AudioSample("\oscBumper\carBonk.wav")
playerBonk = AudioSample("\oscBumper\playerBonk.wav")
platformBonk = AudioSample("\oscBumper\platform.wav")
carnival = AudioSample("\oscBumper\carnival.wav")
carnival.loop(times = -1, start = 0, size = -1, voice = 0)

# platform parameters
platformWidth  = 1000
platformHeight = 680       
carRadius      = 30        

# behavior parameters
separationFactor = 0.001   # how quickly they separate
alignmentFactor  = 0.05    # aligning with other NPCs
cohesionFactor   = 0.005   # moving to attraction point
frictionFactor   = 1.1     # friction
 
# car distance parameters
minSeparation = carRadius * 2 # min comfortable distance between two cars
carThreshold  = 1             # cars closer than this are grouped

# generation parameters
numNPCs     = 0            # number of NPC
npcColor    = Color.BLACK  # default is black

# player parameters
numPlayers  = 10           # number of Players
red         = Color(200, 0, 0)
orange      = Color(255, 130, 0)
yellow      = Color(255, 255, 0)
ligreen     = Color(175, 255, 100)
green       = Color(0, 150, 0)
liblue      = Color(100, 175, 255)
blue        = Color(0, 0, 250)
lipurp      = Color(200, 150, 255)
purp        = Color(150, 0, 150)
pink        = Color(255, 150, 200)
playerColor = [red, orange, yellow, ligreen, green, liblue, blue, lipurp, purp, pink]
playerPorts = [28821, 28822, 28823, 28824, 28825, 28826, 28827, 28828, 28829, 28830]

##### tutorial display #####
tutorial  = Display("Instructions", 263, 680, 1001, 0, Color(250, 200, 150))
rectangle = Rectangle(30, 60, 230, 620, Color(255, 230, 200, 150), True, 20)
introText = TextArea("Welcome to Bump Itz, a virtual \nbumper car simulator! Enter the \nport number of the car color you \nwant. The host address has been \nalready set up for you. To move, \nwave your mouse in the display.", 6, 200)

tutorial.add(rectangle)
tutorial.add(introText, 0, 90)

colorStr = ["Red", "Orange", "Yellow", "Lite Green", "Green", "Lite Blue", "Blue", "Lite Purple", "Purple", "Pink"]
portStr  = ["28821", "28822", "28823", "28824", "28825", "28826", "28827", "28828", "28829", "28830"]

y = 240
for i in range(numPlayers):
   portText  = TextArea("Port: " + portStr[i] + " " + colorStr[i], 1, 200) 
   tutorial.add(portText, 0, y)
   y += 35

##### OSC setup #####
oscIns = []
for i in range(numPlayers):
   port  = playerPorts[i]
   oscIn = OscIn(port)
   oscIns.append(oscIn)
   oscIn.hideMessages()
   #print port

# move players' positions
def movePlayerCar(message):
   global platform
   address  = message.getAddress()
   args     = message.getArguments()
   output   = str(args)
   outArray = output.split(",")

   # check if outputArray has at least 2 arguments to get x and y values
   if len(outArray) >= 3:
      # extract port number from address
      port = int(address.split("/")[-1])
      
      for player in platform.players:
         # check if player port matches received port
         if player.port == port:
            arrayMsg = outArray[0]
            # stripping the strings to only numbers, originally had {} and ()
            arg1 = float(outArray[1].replace("[", "").replace("]", "").replace(")", "").strip())
            arg2 = float(outArray[2].replace("[", "").replace("]", "").replace(")", "").strip())
            # test prints to console to double check
            print arg1, arg2
              
            # mapping values and updating Player's attraction point
            carX = arg1
            carY = arg2
            # test prints
            print carX, carY
            player.playerPoint = complex(carX, carY)
      
# function calls
oscIns[0].onInput("/28821", movePlayerCar)
oscIns[1].onInput("/28822", movePlayerCar)
oscIns[2].onInput("/28823", movePlayerCar)
oscIns[3].onInput("/28824", movePlayerCar)
oscIns[4].onInput("/28825", movePlayerCar)
oscIns[5].onInput("/28826", movePlayerCar)
oscIns[6].onInput("/28827", movePlayerCar)      
oscIns[7].onInput("/28828", movePlayerCar)
oscIns[8].onInput("/28829", movePlayerCar)
oscIns[9].onInput("/28830", movePlayerCar)

##### the simulator's Platform #####
class BumperPlatform:
   
   def __init__(self, title = "", width = 600, height = 600, frameRate=30):
      
      # display setup
      self.display = Display(title, width, height, 0, 0, Color(250, 200, 150))
      self.rect    = Rectangle(75, 75, width - 75, height - 75, Color(255, 230, 200, 150), True, 50)
      self.horizLine1 = Line(0, int(height * 0.25), width, int(height * 0.25), Color.BLACK, 1)
      self.horizLine2 = Line(0, int(height * 0.50), width, int(height * 0.50), Color.BLACK, 1)
      self.horizLine3 = Line(0, int(height * 0.75), width, int(height * 0.75), Color.BLACK, 1)
      self.vertiLine1 = Line(int(width * 0.25), 0, int(width * 0.25), height, Color.BLACK, 1)
      self.vertiLine2 = Line(int(width * 0.50), 0, int(width * 0.50), height, Color.BLACK, 1)
      self.vertiLine3 = Line(int(width * 0.75), 0, int(width * 0.75), height, Color.BLACK, 1)
      
      # adding everything to display
      self.display.add(self.rect)
      self.display.add(self.horizLine1)
      self.display.add(self.horizLine2)
      self.display.add(self.horizLine3)
      self.display.add(self.vertiLine1)
      self.display.add(self.vertiLine2)
      self.display.add(self.vertiLine3)
      
      # list of NPCs and Players
      self.npcs    = []
      self.players = [] 
  
      # attraction point for NPCs (initially Platform center)
      self.attractPoint = complex(width/2, height/2)  
      
      # simulation timer
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
         player.sense(self.players, self.npcs, player.playerPoint)
         player.act(self.display)   
                
   def moveAttractionPoint(self, x, y):
      # moves NPCs attraction point
      self.attractPoint = complex(x, y)

##### the npc class setup #####
class NPC:
   # audio files
   global carBonk, platformBonk
   
   def __init__(self, x, y, radius, color, initVelocityX=1, initVelocityY=1):
      # car setup
      self.circle = Circle(x, y, radius, color, True) 
      iconSize    = int(carRadius * 1.5)
      self.icon   = Icon("carIcon.png", iconSize)

      # set car size and position
      self.radius      = radius                # car radius
      self.coordinates = complex(x, y)    # car coordinates (x, y)

      # car velocity (x, y)
      self.velocity = complex(initVelocityX, initVelocityY)  
   
   ##### inspired by boids #####
   def sense(self, players, npcs, center):
  
      # 1. Rule of Separation - move away from other cars
      self.separation_players = self.rule1_Separation(players)
      self.separation_npcs    = self.rule1_Separation(npcs)
  
      # 2. Rule of Alignment - aligning with other cars
      self.alignment_players = self.rule2_Alignment(players)
      self.alignment_npcs    = self.rule2_Alignment(npcs)
  
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
         platformBonk.play()
      elif x > platformWidth - self.radius:
         x = platformWidth - self.radius
         self.velocity = complex(-self.velocity.real, self.velocity.imag)
         platformBonk.play()
      if y < self.radius:
         y = self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag) 
         platformBonk.play()
      elif y > platformHeight - self.radius:
         y = platformHeight - self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag)
         platformBonk.play()
      
      iconCenterX = self.radius * 0.72
      iconCenterY = self.radius * 0.8
   
      # act 
      display.move(self.icon, int(x - iconCenterX), int(y - iconCenterY))
      display.move(self.circle, int(x), int(y))
  
   ##### defining rules #####
   def rule1_Separation(self, npcs):
      # holds new velocity
      newVelocity = complex(0, 0) 
      
      for npc in npcs:
         separation = self.distance(npc)
         # checks if too close to other cars
         if separation < minSeparation and npc != self:
            newVelocity = newVelocity - (npc.coordinates - self.coordinates)
            carBonk.play()  
      
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
            numLocalCars  = numLocalCars + 1     
           
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

##### the player class setup #####
class Player:
   # audio file
   global playerBonk, platformBonk 
   def __init__(self, x, y, radius, color, port, initVelocityX=1, initVelocityY=1):
      # car setup
      self.circle = Circle(x, y, radius, color, True) 
      iconSize    = int(carRadius * 1.5)
      self.icon   = Icon("carIcon.png", iconSize)

      # set car size and position
      self.radius      = radius                # car radius
      self.coordinates = complex(x, y)    # car coordinates (x, y)
      
      # player's corresponding port
      self.port = port

      # car velocity (x, y)
      self.velocity = complex(initVelocityX, initVelocityY)  
      
      # attraction point for Players (initially, Platform center)
      self.playerPoint = complex(platformWidth/2, platformHeight/2)
   
   # moves Player's attraction point
   def movePlayer(self, x, y):
      self.playerPoint = complex(x, y)

   ##### inspired by boids #####
   def sense(self, players, npcs, center):
      
      # 1. Rule of Separation - move away from other cars
      self.separation_players = self.rule1_Separation(players)
      self.separation_npcs    = self.rule1_Separation(npcs)
  
      # 2. Rule of Alignment - aligning with other cars
      self.alignment_players = self.rule2_Alignment(players)
      self.alignment_npcs    = self.rule2_Alignment(npcs)
  
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
      if x < self.radius:
         x = self.radius
         self.velocity = complex(-self.velocity.real, self.velocity.imag)
         platformBonk.play()
      elif x > platformWidth - self.radius:
         x = platformWidth - self.radius
         self.velocity = complex(-self.velocity.real, self.velocity.imag) 
         platformBonk.play()
      if y < self.radius:
         y = self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag)
         platformBonk.play()
      elif y > platformHeight - self.radius:
         y = platformHeight - self.radius
         self.velocity = complex(self.velocity.real, -self.velocity.imag) 
         platformBonk.play()
         
      iconCenterX = self.radius * 0.72
      iconCenterY = self.radius * 0.8

      # act
      display.move(self.icon, int(x - iconCenterX), int(y - iconCenterY))
      display.move(self.circle, int(x), int(y))
  
   ##### defining rules #####
   def rule1_Separation(self, players):
      # holds new velocity
      newVelocity = complex(0, 0)  
      
      for player in players:    
         separation = self.distance(player)
         # checks if too close to other players
         if separation < minSeparation and player != self:
            newVelocity = newVelocity - (player.coordinates - self.coordinates)
            playerBonk.play() 
            
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
            numLocalCars  = numLocalCars + 1     
           
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

##### start simulator #####
platform = BumperPlatform(title="Bump Itz", width=platformWidth, height=platformHeight)

# create Players
for i in range(0, numPlayers):
   # assign specific port numbers
   port = playerPorts[i]
   
   # get random spawn position
   x = randint(0, platformWidth)
   y = randint(0, platformHeight)
  
   # create a car with these parameters
   player = Player(x, y, carRadius, playerColor[i], port, 1, 1)
   platform.addPlayer(player)
  
# create NPCs
for i in range(0, numNPCs):
   # get random position for this car
   x = randint(0, platformWidth)
   y = randint(0, platformHeight)
  
   # create a car with random position and velocity
   npc = NPC(x, y, carRadius, npcColor, 0.25, 0.25)
   platform.addNPC(npc)

# animate cars
platform.start()