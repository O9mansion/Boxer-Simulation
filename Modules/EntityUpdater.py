from .Entityhandler import Entitys, PreviousState
from .Boxersmodules import ReuseFunctions
import time
from .classes import Boxer, StimulationActionPair
import math

# Return the base thinking time for the Ai's
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
        ),

        #Right hand of boxer 1 to right hand of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.right_hand.position,
            Boxer1.hands_radius,
            Boxer2.right_hand.position,
            Boxer2.hands_radius
        ),

        #Right hand of boxer 1 to left hand of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.right_hand.position,
            Boxer1.hands_radius,
            Boxer2.left_hand.position,
            Boxer2.hands_radius
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
        ),

        #Right hand of boxer 1 to right hand of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.left_hand.position,
            Boxer1.hands_radius,
            Boxer2.right_hand.position,
            Boxer2.hands_radius
        ),

        #Right hand of boxer 1 to left hand of boxer 2
        ReuseFunctions.CirclesCollitionCheck(
            Boxer1.left_hand.position,
            Boxer1.hands_radius,
            Boxer2.left_hand.position,
            Boxer2.hands_radius
        )
    ]
    Boxer2RightCheck = [
        #Right hand of boxer 2 to head of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.head_position,
            Boxer1.head_radius
        ),

        #Right hand of boxer 2 to body of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.position,
            Boxer1.body_radius
        ),

        #Right hand of boxer 2 to right hand of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.right_hand.position,
            Boxer1.hands_radius
        ),

        #Right hand of boxer 2 to left hand of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.right_hand.position,
            Boxer2.hands_radius,
            Boxer1.left_hand.position,
            Boxer1.hands_radius
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

    ReuseFunctions.ResolveHandColition(Boxer1.right_hand, Boxer1RightCheck, Boxer2, PreviousState.boxer_1_right_hand_position, Boxer1.right_hand.position)

def UpdateAIStates(Boxer1: Boxer, Boxer2:Boxer, PreviousPosBoxer1, PreviousPosBoxer2):
    if Boxer.state == "Knocked":
        Boxer.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Boxer.max_mental_clearness,Boxer.active_mental_clearness)
        Boxer.ticks_to_next_action += ReuseFunctions.LoadSetting("Boxer knock down penalty")
        Boxer.state = "Thinking"

    if Boxer.state == "Action":
        #Now we gotta check first if the boxer has any memory.
        if Boxer.memory.active_actions < 0:
            ActGroup = ReuseFunctions.GenerateRandActonGroup()
            Stimulation = ReuseFunctions.CreateStimulation(Boxer1, Boxer2, PreviousPosBoxer1, PreviousPosBoxer2)

            StimulationActionGroup = StimulationActionPair(ActGroup, Stimulation)

            Boxer.memory.add_memory(StimulationActionGroup)
            Boxer.memory.active_actions = 1

        #Now we can judge if we have a propper action we can take
        BestAction = ReuseFunctions.ReturnBestSituationBasedOnStimuli(ReuseFunctions.CreateStimulation(Boxer1, Boxer2, PreviousPosBoxer1, PreviousPosBoxer2), Boxer1.memory)

        Index, Value, Flipped = BestAction

#Now we need to tick everithing to update it.
def Tick():
    #Check to see if any body parts are intersecting, discluding the hands.
    CheckForCollitions(Entitys[0], Entitys[1])

    #Now we need to check the hands and if they intersect with any of the boxers based on state.... AAAAAAAA
    CheckForHandCollitions(Entitys[0], Entitys[1])

    #Update the AI's States
    UpdateAIStates(Entitys[0], Entitys[1], PreviousState.boxer_1_position, PreviousState.boxer_2_position) #Boxer1
    UpdateAIStates(Entitys[1], Entitys[0],PreviousState.boxer_2_position, PreviousState.boxer_1_position) #Boxer2

def Test(TestType):
    Setup()
    if TestType == "Movement":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.move(10,"F")
            time.sleep(0.2)

    elif TestType == "Puntching":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.puntch("R")
                Entity.puntch("L")
            time.sleep(1)

    elif TestType == "HeadBodyHand":
        boxer_one = Entitys[0]
        boxer_two = Entitys[1]

        for _ in range(3):
            boxer_one.move(12)
            time.sleep(0.2)
            boxer_one.move(12)
            time.sleep(0.2)
            boxer_one.move(12)

            boxer_one.puntch("R")

            boxer_one.puntch("L")
            time.sleep(2)
    
    elif TestType == "Rotation And Moving":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.move(10)
                Entity.rotate(-5)
            time.sleep(0.2)