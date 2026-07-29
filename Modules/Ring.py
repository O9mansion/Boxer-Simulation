import random
import Modules.classes as Classes
from Modules.classes import Boxer, Memory
import Modules.Boxersmodules.ReuseFunctions as ReuseFunctions
import Modules.Entityhandler as EntityHandler
import Modules.EntityTicker as EntityTicker
import Modules.EntityUpdater as EntityUpdater

Boxer1:Boxer = None
Boxer2:Boxer = None

def Setup():
    global Boxer1, Boxer2

    #Create the boxers and add them to the entity registry for uhhhh, Registring em!
    Boxer1 = EntityHandler.CreateBoxer([200, 400 + random.randint(-120,120)],90 + random.randint(-40,40))
    Boxer2 = EntityHandler.CreateBoxer([600,400 + random.randint(-120,120)],270 + random.randint(-40,40))

def ClearAndSetup(Boxer1Mem,Boxer2Mem):
    global Boxer1, Boxer2

    #Pause the Simulation so that we can safely remove the boxers
    EntityTicker.Pause()

    EntityHandler.RemoveBoxer(Boxer1)
    EntityHandler.RemoveBoxer(Boxer2)

    #Might as well use the same function to spawn them
    Setup()

    #Give them back their memory to continue fighting like the once did.
    Boxer1.memory = Boxer1Mem
    Boxer2.memory = Boxer2Mem

    #Give them their think times back
    EntityUpdater.Setup()

    #Release the Simulation and carry on the attack!
    EntityTicker.Play()