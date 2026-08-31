from .classes import Boxer, Memory, Hand, previous_ring_state
from .Boxersmodules import ReuseFunctions
import math

Entitys = []

PreviousState = previous_ring_state()

def Update():
    global PreviousState, Entitys

    PreviousState.Update(Entitys[0], Entitys[1])

def CreateBoxer(Position, Rotation):
    global Entitys

    NewBoxer = Boxer()

    NewBoxer.position = Position
    NewBoxer.rotation = Rotation
    NewBoxer.boxer_id = ReuseFunctions.MakeObjectID()

    NewBoxer.memory = Memory(max_action_memory=16)

    NewBoxer.max_mental_clearness = 100
    NewBoxer.max_stamina = 100

    NewBoxer.active_mental_clearness = 100
    NewBoxer.active_stamina = 100

    NewBoxer.available_mental_clearness = 100
    NewBoxer.available_stamina = 100

    NewBoxer.head_radius = 35
    NewBoxer.body_radius = 50
    NewBoxer.hands_radius = 13
    NewBoxer.max_speed = ReuseFunctions.LoadSetting("Max boxer movement speed")
    NewBoxer.max_rotation_speed = ReuseFunctions.LoadSetting("Max boxer rotation speed")
    NewBoxer.friction = ReuseFunctions.LoadSetting("Boxer friction")
    NewBoxer.max_puntching_distance = ReuseFunctions.LoadSetting("Max puntching distance")
    NewBoxer.puntching_ierations = ReuseFunctions.LoadSetting("Puntching iterations")
    NewBoxer.puntching_distance_growth_factor = ReuseFunctions.LoadSetting("Puntching growth factor")
    NewBoxer.puntching_returning_speed = ReuseFunctions.LoadSetting("Puntching return speed")
    NewBoxer.puntch_stamina_drain = ReuseFunctions.LoadSetting("Boxer puntching stamina cost")
    NewBoxer.stamina_recover_speed = ReuseFunctions.LoadSetting("Boxer stamina recover")
    NewBoxer.mental_clearness_recover_speed = ReuseFunctions.LoadSetting("Boxer mental clearness recover")
    NewBoxer.stimuli_to_stimuless_max_value = ReuseFunctions.LoadSetting("Stimuli to stimuless max value")
    NewBoxer.boxer_mass = ReuseFunctions.LoadSetting("Boxer mass")
    NewBoxer.moment_of_inertia = ReuseFunctions.LoadSetting("Boxers moment of inertia")
    NewBoxer.hand_air_time = ReuseFunctions.LoadSetting("Hand air time")
    NewBoxer.round_ticks = ReuseFunctions.LoadSetting("Round time in ticks")

    x, y = Position

    #Head
    distance = 30
    rotation_rad = math.radians(Rotation)
    dx = math.sin(rotation_rad) * distance
    dy = -math.cos(rotation_rad) * distance

    NewBoxer.head_position = [x+dx, y+dy]

    #Hands
    hand_mass = ReuseFunctions.LoadSetting("Hand mass")
    forward_distance = 50
    side_distance = 50

    forward_rad = math.radians(Rotation)
    right_rad = math.radians(Rotation + 90)

    fx = math.sin(forward_rad) * forward_distance
    fy = -math.cos(forward_rad) * forward_distance

    rx = math.sin(right_rad) * side_distance
    ry = -math.cos(right_rad) * side_distance

    left_hand_position = [
        x + fx - rx,
        y + fy - ry
    ]

    right_hand_position = [
        x + fx + rx,
        y + fy + ry
    ]

    NewBoxer.left_hand = Hand(
        position=left_hand_position,
        owner_id=NewBoxer.boxer_id,
        state="Idle",
        mass=hand_mass
    )

    NewBoxer.right_hand = Hand(
        position=right_hand_position,
        owner_id=NewBoxer.boxer_id,
        state="Idle",
        mass=hand_mass
    )

    Entitys.append(NewBoxer)

    return NewBoxer.boxer_id

def RemoveBoxer(Boxer):
    if Boxer is None:
        return False

    if Boxer not in Entitys:
        return False

    position = Entitys.index(Boxer)
    Entitys.pop(position)
    return True