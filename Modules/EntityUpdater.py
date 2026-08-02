from .Entityhandler import Entitys, PreviousState
from .Boxersmodules import ReuseFunctions
import time
from .classes import Boxer, StimulationActionPair, ActionGroup
import math
import copy

MatchWon = None

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
        ),
        #Left hand of boxer 2 to right hand of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.left_hand.position,
            Boxer2.hands_radius,
            Boxer1.right_hand.position,
            Boxer1.hands_radius
        ),

        #Left hand of boxer 2 to left hand of boxer 1
        ReuseFunctions.CirclesCollitionCheck(
            Boxer2.left_hand.position,
            Boxer2.hands_radius,
            Boxer1.left_hand.position,
            Boxer1.hands_radius
        )
    ]

    ReuseFunctions.ResolveHandColition(
        Boxer1.right_hand,
        Boxer1,
        Boxer1RightCheck,
        Boxer2, PreviousState.boxer_1_right_hand_position,
        Boxer1.right_hand.position,
        PreviousState.boxer_1_right_hand_position
    )
    ReuseFunctions.ResolveHandColition(
        Boxer1.left_hand,
        Boxer1,
        Boxer1LeftCheck,
        Boxer2, PreviousState.boxer_1_left_hand_position,
        Boxer1.left_hand.position,
        PreviousState.boxer_1_left_hand_position
    )
    ReuseFunctions.ResolveHandColition(
        Boxer2.right_hand,
        Boxer2,
        Boxer2RightCheck,
        Boxer1, PreviousState.boxer_2_right_hand_position,
        Boxer2.right_hand.position,
        PreviousState.boxer_2_right_hand_position
    )
    ReuseFunctions.ResolveHandColition(
        Boxer2.left_hand,
        Boxer2,
        Boxer2LeftCheck,
        Boxer1, PreviousState.boxer_2_left_hand_position,
        Boxer2.left_hand.position,
        PreviousState.boxer_2_left_hand_position
    )

def AiCheck(Boxer1: Boxer):
    x, y = Boxer1.position
    ring_x, ring_y = [ReuseFunctions.LoadSetting("Screen Size X"), ReuseFunctions.LoadSetting("Screen Size Y")]
    percentage = 105

    x2_part = (ring_x / percentage) * 100
    x1_part = ring_x - x2_part

    y2_part = (ring_y / percentage) * 100
    y1_part = ring_y - y2_part

    ring_center_x = (x1_part + x2_part) / 2
    ring_center_y = (y1_part + y2_part) / 2

    x_radius = (x2_part - x1_part) / 2
    y_radius = (y2_part - y1_part) / 2

    dx = x - ring_center_x
    dy = y - ring_center_y

    normalized_x = dx / x_radius if x_radius > 0 else 0
    normalized_y = dy / y_radius if y_radius > 0 else 0

    is_in_ring = (normalized_x * normalized_x + normalized_y * normalized_y) <= 1

    if not is_in_ring:
        Boxer1.state = "PassedOut"

def UpdateAIStates(Boxer1: Boxer, Boxer2:Boxer, PreviousPosBoxer1, PreviousPosBoxer2):
    global MatchWon
    if Boxer1.state == "PassedOut":
            Boxer1.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Boxer1.max_mental_clearness,Boxer1.active_mental_clearness)
            Boxer1.state = "Thinking"
    
            RingCenter = [ReuseFunctions.LoadSetting("Screen Size X"),ReuseFunctions.LoadSetting("Screen Size Y")]
            DistanceBefore = ReuseFunctions.DistanceCheckCircles(Boxer1.pos_before_executing_action_group, RingCenter)
            DistanceNow = ReuseFunctions.DistanceCheckCircles(Boxer1.position, RingCenter)
    
            Boxer1.current_executing_action_group_new_points += (DistanceNow-DistanceBefore)/2
            Boxer1.current_executing_action_group_new_points -= 20
    
            Boxer2.current_executing_action_group_new_points += 10
            
            idx = Boxer1.current_executing_action_group_index
            if idx is not None and idx < len(Boxer1.memory.stimulation_action_pairs):
                StimActionGroupUpdate = Boxer1.memory.stimulation_action_pairs[idx]
                StimActionGroupUpdate.points += Boxer1.current_executing_action_group_new_points
            
            Boxer1.current_executing_action_group_new_points = 0
    
            idx = Boxer2.current_executing_action_group_index
            if idx is not None and idx < len(Boxer2.memory.stimulation_action_pairs):
                StimActionGroupUpdate = Boxer2.memory.stimulation_action_pairs[idx]
                StimActionGroupUpdate.points += Boxer2.current_executing_action_group_new_points
                        
            Boxer2.current_executing_action_group_new_points = 0
    
            MatchWon = Boxer2

    if Boxer1.state == "Knocked":
        Boxer1.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Boxer1.max_mental_clearness,Boxer1.active_mental_clearness)
        Boxer1.ticks_to_next_action += ReuseFunctions.LoadSetting("Boxer knock down penalty")
        Boxer1.state = "Thinking"

    if Boxer1.state == "Action":
        FoundBestAction = False

        #Now we gotta check first if the boxer has any memory.
        if Boxer1.memory.active_actions <= 0:
            ActGroup = ReuseFunctions.GenerateRandActonGroup()
            Stimulation = ReuseFunctions.CreateStimulation(Boxer1, Boxer2, PreviousPosBoxer1, PreviousPosBoxer2)

            StimulationActionGroup = StimulationActionPair(Stimulation, ActGroup, 250)

            Boxer1.memory.add_memory(StimulationActionGroup)

        #Now we can judge if we have a propper action we can take
        BestAction = ReuseFunctions.ReturnBestSituationBasedOnStimuli(ReuseFunctions.CreateStimulation(Boxer1, Boxer2, PreviousPosBoxer1, PreviousPosBoxer2), Boxer1.memory)

        Index, Value, Flipped = BestAction
        
        if Flipped:
            Index-= Boxer1.memory.active_actions

        if Value < Boxer1.stimuli_to_stimuless_max_value:
            ActG:ActionGroup = Boxer1.memory.stimulation_action_pairs[Index].action
            Rot = copy.deepcopy(ActG.rotation)
            Move = copy.deepcopy(ActG.movement)
            Att = copy.deepcopy(ActG.attacking)
                        
            Boxer1.current_executing_action_group = ActionGroup(rotation=Rot, movement=Move, attacking=Att)
            FoundBestAction = True
        else:
            ActGroup = ReuseFunctions.GenerateRandActonGroup()
            Stimulation = ReuseFunctions.CreateStimulation(Boxer1, Boxer2, PreviousPosBoxer1, PreviousPosBoxer2)
            
            StimulationActionGroup = StimulationActionPair(Stimulation, ActGroup, 250)
            
            Boxer1.memory.add_memory(StimulationActionGroup)

            ActG:ActionGroup = Boxer1.memory.stimulation_action_pairs[Index].action
            Rot = copy.deepcopy(ActG.rotation)
            Move = copy.deepcopy(ActG.movement)
            Att = copy.deepcopy(ActG.attacking)
            
            Boxer1.current_executing_action_group = ActionGroup(rotation=Rot, movement=Move, attacking=Att)
            FoundBestAction = True

        if FoundBestAction:
            Boxer1.state = "Fighting"
            Boxer1.pos_before_executing_action_group = Boxer1.position
            Boxer1.current_executing_action_group_index = Index
        else:
            print("Boxer could not find best action")

    elif Boxer1.state == "Fighting":
        # Create copies of the lists so we don't erase the AI's permanent memory
        Rotation = Boxer1.current_executing_action_group.rotation
        Movement = Boxer1.current_executing_action_group.movement
        Puntches = Boxer1.current_executing_action_group.attacking
        Index = Boxer1.current_executing_action_group_index

        if len(Rotation) == 0 and len(Movement) == 0 and len(Puntches) == 0:
            group:StimulationActionPair = Boxer1.memory.stimulation_action_pairs[Index]

            rot = group.action.rotation
            move = group.action.movement
            punt = group.action.attacking

            if len(rot) == 0 and len(move) == 0 and len(punt) == 0:
                pass

        def EndingToThinkingAgain():
            Boxer1.ticks_to_next_action = ReuseFunctions.ReturnThinkingTime(Boxer1.max_mental_clearness,Boxer1.active_mental_clearness)
            Boxer1.state = "Thinking"

            RingCenter = [ReuseFunctions.LoadSetting("Screen Size X"),ReuseFunctions.LoadSetting("Screen Size Y")]
            DistanceBefore = ReuseFunctions.DistanceCheckCircles(Boxer1.pos_before_executing_action_group, RingCenter)
            DistanceNow = ReuseFunctions.DistanceCheckCircles(Boxer1.position, RingCenter)

            Boxer1.current_executing_action_group_new_points += (DistanceNow-DistanceBefore)/2
        
            idx = Boxer1.current_executing_action_group_index
            if idx is not None and idx < len(Boxer1.memory.stimulation_action_pairs):
                StimActionGroupUpdate = Boxer1.memory.stimulation_action_pairs[idx]
                StimActionGroupUpdate.points += Boxer1.current_executing_action_group_new_points
        
            Boxer1.current_executing_action_group_new_points = 0
            


        #If they are all the same length then we can just execute them all

        if len(Rotation) == len(Movement) == len(Puntches):
            if len(Rotation) == 0 and len(Movement) == 0 and len(Puntches) == 0:
                EndingToThinkingAgain()
                return

            # Execute the puntches first - ALWAYS pop them so we don't get stuck
            if Puntches:
                if Puntches[0] == "L":
                    if Boxer1.left_hand.state == "Idle":
                        Boxer1.puntch("L")
                    Puntches.pop(0)
                elif Puntches[0] == "R":
                    if Boxer1.right_hand.state == "Idle":
                        Boxer1.puntch("R")
                    Puntches.pop(0)
                elif Puntches[0] == "N":
                    Puntches.pop(0)

            # Then movement
            if Movement:
                if Movement[0] == 0:
                    Movement.pop(0)
                elif isinstance(Movement[0], list):
                    direction, distance = Movement[0]
                    Boxer1.move(5, direction)
                    Movement[0][1] -= 1
                    if Movement[0][1] <= 0:
                        Movement.pop(0)   

            # Then Rotation
            if Rotation:
                if Rotation[0] == 0:
                    Rotation.pop(0)
                elif isinstance(Rotation[0], list):
                    direction, distance = Rotation[0]
                    if direction == "R":
                        Boxer1.rotate(2)
                    else:
                        Boxer1.rotate(-2)
                    Rotation[0][1] -= 1
                    if Rotation[0][1] <= 0:
                        Rotation.pop(0)
        else: #Now we gotta find the Longest one(s) and execute them first
            if len(Rotation) == 0 and len(Movement) == 0 and len(Puntches) == 0:
                EndingToThinkingAgain()
                return

            all_lists = [
                (len(Rotation), "Rotation", Rotation),
                (len(Movement), "Movement", Movement),
                (len(Puntches), "Puntches", Puntches)
            ]

            all_lists.sort(key=lambda x: x[0], reverse=True)

            Longest = all_lists[0]
            Seccondlongest = all_lists[1]
            BaseSize = all_lists[2]

            SeccondRun = Seccondlongest == Longest

            if Longest[1] == "Puntches":
                if Puntches[0] == "L":
                    if Boxer1.left_hand.state == "Idle":
                        Boxer1.puntch("L")
                        Puntches.pop(0)
                elif Puntches[0] == "R":
                    if Boxer1.right_hand.state == "Idle":
                        Boxer1.puntch("R")
                        Puntches.pop(0)
                elif Puntches[0] == "N":
                    Puntches.pop(0)
            elif Longest[1] == "Movement":
                if Movement[0] == 0:
                    Movement.pop(0)
                elif isinstance(Movement[0], list): # Make sure it's a list [Dir, Dist]
                    direction, distance = Movement[0]
                    Boxer1.move(5, direction)
                    Movement[0][1] -= 1
                    if Movement[0][1] <= 0:
                        Movement.pop(0)
            elif Longest[1] == "Rotation":
                if Rotation[0] == 0:
                    Rotation.pop(0)
                elif isinstance(Rotation[0], list): # Make sure it's a list [Dir, Dist]
                    direction, distance = Rotation[0]
                    if direction == "R":
                        Boxer1.rotate(2)
                    else:
                        Boxer1.rotate(-2)
                    Rotation[0][1] -= 1
                    if Rotation[0][1] <= 0:
                        Rotation.pop(0)

            if SeccondRun:
                if Seccondlongest[1] == "Puntches":
                    if Puntches[0] == "L":
                        if Boxer1.left_hand.state == "Idle":
                            Boxer1.puntch("L")
                    elif Puntches[0] == "R":
                        if Boxer1.right_hand.state == "Idle":
                            Boxer1.puntch("R")
                    elif Puntches[0] == "N":
                        Puntches.pop(0)
                elif Seccondlongest[1] == "Movement":
                    if Movement[0] == 0:
                        Movement.pop(0)
                    elif isinstance(Movement[0], list): # Make sure it's a list [Dir, Dist]
                        direction, distance = Movement[0]
                        Boxer1.move(5, direction)
                        Movement[0][1] -= 1
                        if Movement[0][1] <= 0:
                            Movement.pop(0)
                elif Seccondlongest[1] == "Rotation":
                    if Rotation[0] == 0:
                        Rotation.pop(0)
                    elif isinstance(Rotation[0], list): # Make sure it's a list [Dir, Dist]
                        direction, distance = Rotation[0]
                        if direction == "R":
                            Boxer1.rotate(2)
                        else:
                            Boxer1.rotate(-2)
                        Rotation[0][1] -= 1
                        if Rotation[0][1] <= 0:
                            Rotation.pop(0)

        
        
#Now we need to tick everithing to update it.
def Tick():
    #Check to see if any body parts are intersecting, discluding the hands.
    CheckForCollitions(Entitys[0], Entitys[1])

    #Now we need to check the hands and if they intersect with any of the boxers based on state
    CheckForHandCollitions(Entitys[0], Entitys[1])

    #Make sure the Ai is still in the ring
    AiCheck(Entitys[0])
    AiCheck(Entitys[1])

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
        boxer_one:Boxer = Entitys[0]
        boxer_two:Boxer = Entitys[1]

        boxer_one.position = [400,400]
        boxer_two.position = [580,470]

        boxer_one.rotation = 90
        boxer_two.rotation = 270

        boxer_one.puntch("R")
        boxer_one.puntch("L")
    
    elif TestType == "Rotation And Moving":
        for l in range(0,10):
            for index, Entity in enumerate(Entitys):
                Entity.move(10)
                Entity.rotate(-5)
            time.sleep(0.2)
