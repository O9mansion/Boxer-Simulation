import random
import Modules.classes as Classes
from Modules.classes import Boxer, Memory
import Modules.Entityhandler as EntityHandler
import Modules.EntityUpdater as EntityUpdater

Boxer1:Boxer = None
Boxer2:Boxer = None

def Setup():
    global Boxer1, Boxer2

    #Create the boxers and add them to the entity registry for uhhhh, Registring em!
    boxer_id_1 = EntityHandler.CreateBoxer([200, 400 + random.randint(-120,120)],90 + random.randint(-40,40))
    boxer_id_2 = EntityHandler.CreateBoxer([600,400 + random.randint(-120,120)],270 + random.randint(-40,40))

    Boxer1 = next(entity for entity in EntityHandler.Entitys if entity.boxer_id == boxer_id_1)
    Boxer2 = next(entity for entity in EntityHandler.Entitys if entity.boxer_id == boxer_id_2)

def ClearAndSetup(Boxer1Mem, Boxer2Mem):
    global Boxer1, Boxer2

    #Pause the Simulation so that we can safely remove the boxers
    import Modules.EntityTicker as EntityTicker
    EntityTicker.Pause()

    old_boxer_1 = Boxer1
    old_boxer_2 = Boxer2

    if old_boxer_1 is not None:
        EntityHandler.RemoveBoxer(old_boxer_1)
    if old_boxer_2 is not None and old_boxer_2 is not old_boxer_1:
        EntityHandler.RemoveBoxer(old_boxer_2)

    #Might as well use the same function to spawn them
    Setup()

    #Give them back their memory to continue fighting like the once did.
    if Boxer1 is not None and Boxer1Mem is not None:
        Boxer1.memory = Boxer1Mem
    if Boxer2 is not None and Boxer2Mem is not None:
        Boxer2.memory = Boxer2Mem

    #Give them their think times back
    EntityUpdater.Setup()

    #Release the Simulation and carry on the attack!
    EntityTicker.Play()


def TickRing():
    if EntityUpdater.MatchWon is not None:
        current_boxers = [entity for entity in EntityHandler.Entitys if isinstance(entity, Boxer)]
        if len(current_boxers) >= 2:
            boxer_1_memory = current_boxers[0].memory
            boxer_2_memory = current_boxers[1].memory
        else:
            boxer_1_memory = Boxer1.memory if Boxer1 is not None else None
            boxer_2_memory = Boxer2.memory if Boxer2 is not None else None

        EntityUpdater.MatchWon = None
        ClearAndSetup(boxer_1_memory, boxer_2_memory)