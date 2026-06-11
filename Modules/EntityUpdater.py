from .Entityhandler import Entitys
from .Boxersmodules import ReuseFunctions
import time
from .classes import Boxer
import math

#NOW WE GET TO DO THE FUN STUFF! PHYSICS AND THE BRAIN LOOP OR WHATEVER! this is gunna be horrible AAAAAAAAAAAAAAAAAAAAAAA
def Setup():
    for Entity in Entitys:
        Entity.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Entity.max_mental_clearness,Entity.active_mental_clearness)

# All collition checks

#Body to Body Collition check
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

# Hand to Hand/body collitions
def CheckForHandCollitions(Boxer1: Boxer, Boxer2: Boxer):
    Boxer1RightCheck = [
        #Right hand of boxer 1 to head of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.right_hand.position,
            Boxer1.hands_radius,
            Boxer2.head_position,
            Boxer2.head_radius
        ),

        #Right hand of boxer 1 to body of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.right_hand.position,
            Boxer1.hands_radius,
            Boxer2.position,
            Boxer2.body_radius
        )
    ]
    Boxer1LeftCheck = [

        # Left hand of boxer 1 to head of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.left_hand.position,
            Boxer1.hands_radius,
            Boxer2.head_position,
            Boxer2.head_radius
        ),

        # Left hand of boxer 1 to body of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.left_hand.position,
            Boxer1.hands_radius,
            Boxer2.position,
            Boxer2.body_radius
        )
    ]
    Boxer2RightCheck = [
        #Right hand of boxer 1 to head of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.head_position,
            Boxer1.head_radius
        ),

        #Right hand of boxer 1 to body of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.position,
            Boxer1.body_radius
        )
    ]
    Boxer2LeftCheck = [

        # Left hand of boxer 1 to head of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.left_hand.position,
            Boxer2.hands_radius,
            Boxer1.head_position,
            Boxer1.head_radius
        ),

        # Left hand of boxer 1 to body of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.left_hand.position,
            Boxer2.hands_radius,
            Boxer1.position,
            Boxer1.body_radius
        )
    ]

    

# NOW WE GOTTA DO PHYSICS AAAAAAAAAAAAAAAAAAAAAAAAAA I'm so cooked....
def Tick():
    CheckForCollitions(Entitys[0], Entitys[1])

    # Hey... That was easy ish enough!
    #Now we need to check the hands and if they intersect with any of the boxers based on state.... AAAAAAAA
    CheckForHandCollitions(Entitys[0], Entitys[1])

def Test(TestType):
    Setup()
    if TestType == "Movement":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.move(10)
            time.sleep(0.2)

    elif TestType == "Puntching":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.puntch("R")
                Entity.puntch("L")
            time.sleep(1)
    
    elif TestType == "Rotation And Moving":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.move(10)
                Entity.rotate(-15)
            time.sleep(0.2)
