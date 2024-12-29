# interface
#
# Author:     Chi Nguyen
# Email:      nguyenct1@g.cofc.edu
# Class:      CITA 284 
# Assignment: Final Project
# Due Date:   26 April 2024
#
# Purpose: User interface for bumperCarsMulti.py
#
# Input:   OSC data from interface.py code

from gui import *
from osc import *

# interface setup
width = 1000
height = 680
numPlayers = 10
interface = Display("Bump Itz Interface", width, height, 0, 0, Color(250, 200, 150))
rectangle = Rectangle(75, 75, width - 75, height - 75, Color(255, 230, 200, 150), True, 50)
horizLine1 = Line(0, int(height * 0.25), width, int(height * 0.25), Color.BLACK, 1)
horizLine2 = Line(0, int(height * 0.50), width, int(height * 0.50), Color.BLACK, 1)
horizLine3 = Line(0, int(height * 0.75), width, int(height * 0.75), Color.BLACK, 1)
vertiLine1 = Line(int(width * 0.25), 0, int(width * 0.25), height, Color.BLACK, 1)
vertiLine2 = Line(int(width * 0.50), 0, int(width * 0.50), height, Color.BLACK, 1)
vertiLine3 = Line(int(width * 0.75), 0, int(width * 0.75), height, Color.BLACK, 1)

# add to interface
interface.add(rectangle)
interface.add(horizLine1)
interface.add(horizLine2)
interface.add(horizLine3)
interface.add(vertiLine1)
interface.add(vertiLine2)
interface.add(vertiLine3)

# tutorial setup
tutorial  = Display("Instructions", 263, 680, 1001, 0, Color(250, 200, 150))
rectangle = Rectangle(30, 60, 230, 620, Color(255, 230, 200, 150), True, 20)
introText = TextArea("Welcome to Bump Itz, a virtual \nbumper car simulator! Enter the /\nport number of the car color you \nwant. The host address has been \nalready set up for you. To move, \nwave your mouse in the display.", 6, 200)

tutorial.add(rectangle)
tutorial.add(introText, 0, 90)

colorStr = ["Red", "Orange", "Yellow", "Lite Green", "Green", "Lite Blue", "Blue", "Lite Purple", "Purple", "Pink"]
portStr  = ["28821", "28822", "28823", "28824", "28825", "28826", "28827", "28828", "28829", "28830"]

y = 240
for i in range(numPlayers):
   portText  = TextArea("Port: " + portStr[i] + " " + colorStr[i], 1, 200) 
   tutorial.add(portText, 0, y)
   y += 35

# osc setup
# ports 28821 - 28830
port = input("Enter desired port: ")
out = OscOut("10.5.195.255", port)

def changeCoords(x, y):
   portAddress = str(port)
   out.sendMessage("/" + portAddress, x, y)

interface.onMouseMove(changeCoords)