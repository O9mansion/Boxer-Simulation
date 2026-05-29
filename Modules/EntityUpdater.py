from .Entityhandler import Entitys
from .Boxersmodules import ReuseFunctions
import time

#NOW WE GET TO DO THE FUN STUFF! PHYSICS AND THE BRAIN LOOP OR WHATEVER! this is gunna be horrible AAAAAAAAAAAAAAAAAAAAAAA
def Setup():
    for Entity in Entitys:
        Entity.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Entity.max_mental_clearness,Entity.active_mental_clearness)

def Start():
    pass

def Test():
    Setup()
    for l in range(0,10):
        for index, Entity in enumerate(Entitys):
            Entity.move(10)
        time.sleep(0.2)
