from .Entityhandler import Entitys
from .Boxersmodules import ReuseFunctions
import time
from .classes import Boxer
import math

#NOW WE GET TO DO THE FUN STUFF! PHYSICS AND THE BRAIN LOOP OR WHATEVER! this is gunna be horrible AAAAAAAAAAAAAAAAAAAAAAA
def Setup():
    for Entity in Entitys:
        Entity.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Entity.max_mental_clearness,Entity.active_mental_clearness)

def CheckForCollitions(Boxer1: Boxer, Boxer2: Boxer):

    collisions = [

        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.head_position,
            Boxer1.head_radius,
            Boxer2.head_position,
            Boxer2.head_radius
        ),

        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.position,
            Boxer1.body_radius,
            Boxer2.position,
            Boxer2.body_radius
        ),

        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.position,
            Boxer1.body_radius,
            Boxer2.head_position,
            Boxer2.head_radius
        ),

        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.head_position,
            Boxer1.head_radius,
            Boxer2.position,
            Boxer2.body_radius
        )
    ]

    for collision in collisions:
        ReuseFunctions.ResolveCollision(Boxer1, Boxer2, collision)




# NOW WE GOTTA DO PHYSICS AAAAAAAAAAAAAAAAAAAAAAAAAA I'm so cooked....
def Tick():
    CheckForCollitions(Entitys[0], Entitys[1])

def Test():
    Setup()
    for l in range(0,10):
        for index, Entity in enumerate(Entitys):
            Entity.move(10)
        time.sleep(0.2)
