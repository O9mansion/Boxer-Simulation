from .classes import Boxer, Memory, Hand
from .Boxersmodules import ReuseFunctions
import math

Entitys = []

def CreateBoxer(Position, Rotation):
    global Entitys

    NewBoxer = Boxer()

    NewBoxer.position = Position
    NewBoxer.rotation = Rotation
    NewBoxer.boxer_id = ReuseFunctions.MakeObjectID()

    NewBoxer.memory = Memory(max_action_memory=6)

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
    NewBoxer.friction = ReuseFunctions.LoadSetting("Boxer friction")

    x, y = Position

    #Head
    distance = 30
    rotation_rad = math.radians(Rotation)
    dx = math.sin(rotation_rad) * distance
    dy = -math.cos(rotation_rad) * distance

    NewBoxer.head_position = [x+dx, y+dy]

    #Hands
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
        state="Idle"
    )

    NewBoxer.right_hand = Hand(
        position=right_hand_position,
        owner_id=NewBoxer.boxer_id,
        state="Idle"
    )

    Entitys.append(NewBoxer)

    return NewBoxer.boxer_id