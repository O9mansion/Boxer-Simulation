import random
import math
from ..classes import ActionGroup, Stimulation, Memory
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

    NewStimulation.angle_to_opponent = FlipRotaion(Stimulation.angle_to_opponent)
    NewStimulation.angle_to_ring_center = FlipRotaion(Stimulation.angle_to_ring_center)
    NewStimulation.relative_opponent_angle = FlipRotaion(Stimulation.relative_opponent_angle)
    NewStimulation.opponent_rotation_speed = Stimulation.opponent_rotation_speed
    NewStimulation.closing_speed = Stimulation.closing_speed
    NewStimulation.distance_to_opponent = Stimulation.distance_to_opponent
    NewStimulation.distance_to_ring_center = Stimulation.distance_to_ring_center
    NewStimulation.self_rotation_speed= Stimulation.self_rotation_speed

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
    
    LowestValue = [None,1000]
    for Index, Item in enumerate(ListOfSituation):
        Diff = CompareTwoStimulations(Stim, Item)
        if Diff < LowestValue[1]:
            LowestValue = [Index,Diff,Item.flipped]

    return LowestValue

def CirclesCollitionCheck(pos1, radius1, pos2, radius2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    distance = math.sqrt(dx * dx + dy * dy)

    return distance < (radius1 + radius2)
