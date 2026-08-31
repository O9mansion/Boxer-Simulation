import random
import math
from ..classes import ActionGroup, Stimulation, Memory, Hand, previous_ring_state, Boxer
import json

def LoadSetting(setting):
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Settings file must contain an object")
            return None

        # Ensure key exists
        if setting not in data:
            print(f"Missing setting: {setting}")
            return None

        value = data[setting]

        return value

    except FileNotFoundError:
        print("File not found")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON")
        return None

currentID = 0
def MakeObjectID():
    global currentID
    PastID = currentID
    currentID += 1
    return PastID

def GenerateRandActonGroup():
        #For rotation they can only rotate between 1-8 Same for movement, while puntching is just L or R
        RotList = []
        MoveList = []
        AttackList = []

        DefiniteMove = random.randint(1,6)

        for Position in range(6):
            RotationAct = 0
            RotationDirections = ["R","L"]
            MovementAct = 0
            MovementDirections = ["F","B","L","R"]
            AttackingAct = "N"

            coinflipR = random.randint(1,4)
            randomRotDir = random.randint(0,len(RotationDirections)-1)
            coinflipM = random.randint(1,4)
            randomMoveDir = random.randint(0,len(MovementDirections)-1)
            coinflipA = random.randint(1,4)

            if coinflipR == 1:
                RotList.append([RotationDirections[randomRotDir],random.randint(1,8)])
            else:
                RotList.append(0)

            if Position == DefiniteMove:
                MoveList.append([MovementDirections[randomMoveDir],random.randint(4,8)])
            else:  
                if coinflipM == 1:
                    MoveList.append([MovementDirections[randomMoveDir],random.randint(1,8)])
                else:
                    MoveList.append(0)
                
            if coinflipA == 1:
                RandSide = random.randint(1,2)
                if RandSide == 1:
                    AttackList.append("R")
                else:
                    AttackList.append("L")
            else:
                AttackList.append("N")

                
        return ActionGroup(RotList, MoveList, AttackList)
            
def FlipRotaion(Ang):
    ProcessedAng = 180 - Ang
    if ProcessedAng < 0:
        ProcessedAng += 360
    return ProcessedAng

def ReturnedFlippedSituation(Sitiuation: Stimulation):
    NewStimulation = Stimulation()

    NewStimulation.angle_to_opponent = FlipRotaion(Sitiuation.angle_to_opponent)
    NewStimulation.angle_to_ring_center = FlipRotaion(Sitiuation.angle_to_ring_center)
    NewStimulation.relative_opponent_angle = FlipRotaion(Sitiuation.relative_opponent_angle)
    NewStimulation.opponent_rotation_speed = Sitiuation.opponent_rotation_speed
    NewStimulation.closing_speed = Sitiuation.closing_speed
    NewStimulation.distance_to_opponent = Sitiuation.distance_to_opponent
    NewStimulation.distance_to_ring_center = Sitiuation.distance_to_ring_center
    NewStimulation.self_rotation_speed = Sitiuation.self_rotation_speed

    NewStimulation.flipped = True

    return NewStimulation

def CompareTwoStimulations(Stim1: Stimulation, Stim2: Stimulation):
    TotalDiffOfRingCenterAng = abs(Stim1.angle_to_ring_center - Stim2.angle_to_ring_center)
    TotalDiffOfRingCenterDis = abs(Stim1.distance_to_ring_center - Stim2.distance_to_ring_center)

    TotalDiffOfOppAng = abs(Stim1.angle_to_opponent - Stim2.angle_to_opponent)
    TotalDiffOfOppDis = abs(Stim1.distance_to_opponent - Stim2.distance_to_opponent)

    TotalDiffSelfRotSpeed = abs(Stim1.self_rotation_speed - Stim2.self_rotation_speed)
    TotalDiffOppRotSpeed = abs(Stim1.opponent_rotation_speed - Stim2.opponent_rotation_speed)

    TotalDiffClosingSpeed = abs(Stim1.closing_speed - Stim2.closing_speed)

    TotalDiff = (TotalDiffOfRingCenterAng+TotalDiffOfRingCenterDis+TotalDiffOfOppAng+TotalDiffOfOppDis+TotalDiffSelfRotSpeed+TotalDiffOppRotSpeed+TotalDiffClosingSpeed) / 2
    return TotalDiff

def ReturnThinkingTime(Max,Current):
    MinThinkingTime = LoadSetting("Minimum thinking time")
    MaxThinkingTime = LoadSetting("Maximum thinking time")
    if MinThinkingTime is not None and MaxThinkingTime is not None:
        ratio = Current / Max
        ThinkingTime = MinThinkingTime - (ratio * (MinThinkingTime - MaxThinkingTime))
        return ThinkingTime
    else:
        raise("One of the values are NONE make sure it is defined in settings!")

def ReturnBestSituationBasedOnStimuli(Stim: Stimulation, Mem: Memory):
    ListOfSituation = []
    #Generate a list of normal Sitiation pairs first
    for Item in Mem.stimulation_action_pairs:
        Sitiuation = Item.stimulation
        ListOfSituation.append(Sitiuation)

    #generate flipped Situation pairs(So ai wont need to store 2 diffent sitiations action pairs for the same thing just flipped!)
    for Item in Mem.stimulation_action_pairs:
        Sitiuation = Item.stimulation
        ListOfSituation.append(ReturnedFlippedSituation(Sitiuation))

    LowestValue = [None,1000,False]
    for Index, Item in enumerate(ListOfSituation):
        Diff = CompareTwoStimulations(Stim, Item)
        if Diff < LowestValue[1]:
            LowestValue = [Index,Diff,Item.flipped]

    return LowestValue

def DistanceCheckCircles(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    distance = math.sqrt(dx * dx + dy * dy)

    return distance

def CirclesCollitionCheck(pos1, radius1, pos2, radius2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    distance = math.sqrt(dx * dx + dy * dy)

    overlap = (radius1 + radius2) - distance

    collided = overlap > 0

    angle = math.atan2(dy, dx)

    return collided, overlap, angle

def AngleBetween(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    angle = math.atan2(dy, dx)  # radians

    return angle

def DiffranceBetweenAngles(ang1, ang2):
    Diff = ang1 - ang2
    return Diff

def ResolveCollision(Boxer1, Boxer2, collision_data):

    collided, overlap, angle = collision_data

    if not collided:
        return

    normal_x = math.cos(angle)
    normal_y = math.sin(angle)

    # Separate overlapping boxers
    correction = overlap / 2

    Boxer1.position[0] -= normal_x * correction
    Boxer1.position[1] -= normal_y * correction

    Boxer2.position[0] += normal_x * correction
    Boxer2.position[1] += normal_y * correction

    # Relative velocity
    rel_vx = Boxer2.current_speed[0] - Boxer1.current_speed[0]
    rel_vy = Boxer2.current_speed[1] - Boxer1.current_speed[1]

    speed_along_normal = (
        rel_vx * normal_x +
        rel_vy * normal_y
    )

    # Already moving apart
    if speed_along_normal > 0:
        return

    restitution = 1 / LoadSetting("Boxer collition loss")

    impulse = -(1 + restitution) * speed_along_normal / 2

    impulse_x = impulse * normal_x
    impulse_y = impulse * normal_y

    Boxer1.current_speed[0] -= impulse_x
    Boxer1.current_speed[1] -= impulse_y

    Boxer2.current_speed[0] += impulse_x
    Boxer2.current_speed[1] += impulse_y

    Boxer1.rotate_body_parts()
    Boxer2.rotate_body_parts()

def AngleAndDirectionBetweenTwoAngles(Ang1,Ang2):
    pass

def ApplyImpulse(
    AffectedBoxer: Boxer,
    Hand: Hand
):
    #get the force at witch the hand is hitting at
    impulse = [
        Hand.hand_speed[0] * Hand.mass,
        Hand.hand_speed[1] * Hand.mass
    ]

    #Deal some Knockback
    AffectedBoxer.current_speed[0] += impulse[0] / AffectedBoxer.boxer_mass
    AffectedBoxer.current_speed[1] += impulse[1] / AffectedBoxer.boxer_mass

    #Now we need to get where the inpact happend relitive to the boxer
    r = [
        Hand.position[0] - AffectedBoxer.position[0],
        Hand.position[1] - AffectedBoxer.position[1]
    ]

    torque = (
        r[0] * impulse[1]
        -
        r[1] * impulse[0]
    )

    AffectedBoxer.current_rotation_speed += (
        torque / AffectedBoxer.moment_of_inertia
    )

def ResolveHandColition(Hand: Hand, Boxer:Boxer, Collitions, AffectedBoxer: Boxer, PreviousPosition, CurrentPosition, HandPrevousPosition):
    #Update hand's speed
    Hand.hand_speed = [
        Hand.position[0] - HandPrevousPosition[0],
        Hand.position[1] - HandPrevousPosition[1]
    ]

    #Collide[0], Overlap[1], Angle[2]
    Case1 = Collitions[0] #Head
    Case2 = Collitions[1] #Body
    Case3 = Collitions[2] #Lhand
    Case4 = Collitions[3] #Rhand

    if Case1[0]:
        if Hand.state == "Swinging":
            Hand.state = "Returning"
            Hand.air_time = 0
            Hand.swing_step = 0
            Hand.swing_step_distance = 0.0


            normal_x = math.cos(Case1[2])
            normal_y = math.sin(Case1[2])
            
            # Separate overlapping boxers
            correction = Case1[1]
            
            Hand.position[0] -= normal_x * correction
            Hand.position[1] -= normal_y * correction

            ApplyImpulse(
                AffectedBoxer,
                Hand
            )
            
            #calculate damage:
            damage = Hand.swing_speed + (DistanceCheckCircles(PreviousPosition, AffectedBoxer.position) - DistanceCheckCircles(CurrentPosition, AffectedBoxer.position))
            #print(f"Previous Distance:{DistanceCheckCircles(PreviousPosition, AffectedBoxer.position)}, Distance:{DistanceCheckCircles(CurrentPosition, AffectedBoxer.position)}")
            #print(f" Hit detected, Swing Speed:{Hand.swing_speed}, Distance between last 2 ticks:{DistanceCheckCircles(PreviousPosition, AffectedBoxer.position) - DistanceCheckCircles(CurrentPosition, AffectedBoxer.position)}, For damage:{damage/2}")
            AffectedBoxer.drain_mental(damage/2)
            AffectedBoxer.state = "Knocked"
            AffectedBoxer.current_executing_action_group_new_points -= Hand.swing_speed/2
            Boxer.current_executing_action_group_new_points += Hand.swing_speed
    elif Case2[0]:
        if Hand.state == "Swinging":
                    Hand.state = "Returning"
                    Hand.air_time = 0
                    Hand.swing_step = 0
                    Hand.swing_step_distance = 0.0
        
        
                    normal_x = math.cos(Case1[2])
                    normal_y = math.sin(Case1[2])
                    
                    # Separate overlapping boxers
                    correction = Case1[1]
                    
                    Hand.position[0] -= normal_x * correction
                    Hand.position[1] -= normal_y * correction

                    ApplyImpulse(
                        AffectedBoxer,
                        Hand
                    )
                    
                    #calculate damage:
                    damage = Hand.swing_speed + (DistanceCheckCircles(PreviousPosition, AffectedBoxer.position) - DistanceCheckCircles(CurrentPosition, AffectedBoxer.position))
                    #print(f"Previous Distance:{DistanceCheckCircles(PreviousPosition, AffectedBoxer.position)}, Distance:{DistanceCheckCircles(CurrentPosition, AffectedBoxer.position)}")
                    #print(f" Hit detected, Swing Speed:{Hand.swing_speed}, Distance between last 2 ticks:{DistanceCheckCircles(PreviousPosition, AffectedBoxer.position) - DistanceCheckCircles(CurrentPosition, AffectedBoxer.position)}, For damage:{damage/2}")
                    AffectedBoxer.drain_stamina(damage/2)
                    AffectedBoxer.state = "Knocked"
                    AffectedBoxer.current_executing_action_group_new_points -= Hand.swing_speed/2
                    Boxer.current_executing_action_group_new_points += Hand.swing_speed
    elif Case3[0]:
        if Hand.state == "Swinging":
                    Hand.state = "Returning"
                    Hand.air_time = 0
                    Hand.swing_step = 0
                    Hand.swing_step_distance = 0.0
        
        
                    normal_x = math.cos(Case1[2])
                    normal_y = math.sin(Case1[2])
                    
                    # Separate overlapping boxers
                    correction = Case1[1]
                    
                    Hand.position[0] -= normal_x * correction
                    Hand.position[1] -= normal_y * correction

                    #To the other boxer
                    ApplyImpulse(
                        AffectedBoxer,
                        Hand
                    )

                    ApplyImpulse(
                        Boxer,
                        Hand
                    )

                    if AffectedBoxer.left_hand.state == "Swinging":
                        AffectedBoxer.left_hand.state = "Returning"
                    elif AffectedBoxer.left_hand.state == "Idle":
                        AffectedBoxer.current_executing_action_group_new_points += 5
    elif Case4[0]:
        if Hand.state == "Swinging":
                    Hand.state = "Returning"
                    Hand.air_time = 0
                    Hand.swing_step = 0
                    Hand.swing_step_distance = 0.0
        
        
                    normal_x = math.cos(Case1[2])
                    normal_y = math.sin(Case1[2])
                    
                    # Separate overlapping boxers
                    correction = Case1[1]
                    
                    Hand.position[0] -= normal_x * correction
                    Hand.position[1] -= normal_y * correction

                    #To the other boxer
                    ApplyImpulse(
                        AffectedBoxer,
                        Hand
                    )

                    ApplyImpulse(
                        Boxer,
                        Hand
                    )

                    if AffectedBoxer.right_hand.state == "Swinging":
                        AffectedBoxer.right_hand.state = "Returning"
                    elif AffectedBoxer.right_hand.state == "Idle":
                        AffectedBoxer.current_executing_action_group_new_points += 5

def CreateStimulation(Boxer:Boxer, Opponante:Boxer, BoxerPreviousPosition, OpponantePreviousPosition):
    WorldCenter = [LoadSetting("Screen Size X"),LoadSetting("Screen Size Y")]
    AngleToRingCenter = AngleBetween(Boxer.position, WorldCenter)
    DistanceToRingCenter = DistanceCheckCircles(Boxer.position, WorldCenter)

    AngleToOpponante = AngleBetween(Boxer.position, Opponante.position)
    DistanceToOpponante = DistanceCheckCircles(Boxer.position, Opponante.position)
    RelitiveOpponanteAngle = DiffranceBetweenAngles(AngleBetween(Boxer.position, Opponante.position), Opponante.rotation)

    SelfRotationSpeed = Boxer.current_rotation_speed
    OpponanteRotationSpeed = Opponante.current_rotation_speed

    ClosingSpeed = (DistanceCheckCircles(BoxerPreviousPosition,OpponantePreviousPosition)-DistanceCheckCircles(Boxer.position, Opponante.position))
    Flipped = False

    NewStimulation = Stimulation(
        angle_to_ring_center=AngleToRingCenter,
        distance_to_ring_center=DistanceToRingCenter,
        angle_to_opponent=AngleToOpponante,
        distance_to_opponent=DistanceToOpponante,
        relative_opponent_angle=RelitiveOpponanteAngle,
        self_rotation_speed=SelfRotationSpeed,
        opponent_rotation_speed=OpponanteRotationSpeed,
        closing_speed=ClosingSpeed,
        flipped=Flipped
    )

    return NewStimulation



    
    