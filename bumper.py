
from osc import *
 
oscIn = OscIn( 58810 )
oscIn.hideMessages()

def msg(message):
    address = message.getAddress()
    args = message.getArguments()
    output = str(args)
    outputArray = output.split(",")
    
    # Check if outputArray has at least 3 elements before accessing them
    if len(outputArray) >= 3:
        arrayMsg = outputArray[0]
        # stripping the strings to only numbers
        arg1 = outputArray[1].replace("[", "").strip()
        arg2 = outputArray[2].replace(")", "").replace("]", "").strip()
        # test prints
        print("arg1: " + arg1)
        print("arg2: " + arg2)
 
oscIn.onInput("/.*", msg)

"""
notes:    
singleplayer: npc cars or obstacles
multiplayer: can choose their color/voice
   old, young, male, female, accents
maybe no music
hit sound effects based on velocity, not placement

"""
"""
Accepting OSC input on IP address 10.5.194.198, at port 57110

SPEED      OSC In - Address: "/master/level" , Argument 0: 0.0 to 1.0 
mapValue - 0 to 10?
DIRECTION  OSC In - Address: "/master/red" ,   Argument 0: 0.0 to 1.0
           LEFT = 0.0 to 0.5 RIGHT = 0.5 to 1.0
mapValue - 0 to screen dimensions

colors mapValue - 0 to 127
RED        OSC In - Address: "/master/red" ,   Argument 0: 0.0 to 1.0
GREEN      OSC In - Address: "/master/green" , Argument 0: 0.0 to 1.0
BLUE       OSC In - Address: "/master/blue" ,  Argument 0: 0.0 to 1.0
"""