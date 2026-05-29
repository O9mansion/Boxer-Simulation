import random
import Modules.classes as Classes
import Modules.Boxersmodules.ReuseFunctions as ReuseFunctions
import Modules.Entityhandler as EntityHandler

Boxer1 = None
Boxer2 = None

def Setup():
    global Boxer1, Boxer2

    #Create the boxers and add them to the entity registry for uhhhh, Registring em!
    Boxer1 = EntityHandler.CreateBoxer([200, 400 + random.randint(-120,120)],90 + random.randint(-40,40))
    Boxer2 = EntityHandler.CreateBoxer([600,400 + random.randint(-120,120)],270 + random.randint(-40,40))