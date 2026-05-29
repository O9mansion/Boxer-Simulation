from dataclasses import dataclass, field
from typing import List, Optional, Literal
import math


#So stimulation will be 8 values
#1. Angle to ring center
#2. Distance to ring center
#3. Angle to opponent
#4. Distance to opponent
#5. Relitive opponent angle
#6. Self Rotation speed
#7. Opponent Rotation Speed
#8. Closing speed

@dataclass
class Stimulation:
    angle_to_ring_center: float = 0
    distance_to_ring_center: float = 0

    angle_to_opponent: float = 0
    distance_to_opponent: float = 0

    relative_opponent_angle: float = 0

    self_rotation_speed: float = 0
    opponent_rotation_speed: float = 0

    closing_speed: float = 0
    flipped: bool = False


RotationDirection = Literal["L", "R"]
MovementDirection = Literal["F", "B", "L", "R"]
AttackDirection = Literal["L", "R", "N"]

# So this will be a list of Rotation, Movement and Attacking, each list gets 6 action rows to preform
@dataclass
class ActionGroup:

    rotation: List[Optional[list]] = field(
        default_factory=lambda: [None] * 6
    )

    movement: List[Optional[list]] = field(
        default_factory=lambda: [None] * 6
    )

    attacking: List[AttackDirection] = field(
        default_factory=lambda: ["N"] * 6
    )


#Just a pair to be stored more simply
@dataclass
class StimulationActionPair:
    stimulation: Stimulation
    action: ActionGroup
    points: float
    

#All Stim Act pairs together
@dataclass
class Memory:
    max_action_memory: int

    stimulation_action_pairs: List[StimulationActionPair] = field(
        default_factory=list
    )

    def add_memory(self, pair: StimulationActionPair):

        self.stimulation_action_pairs.append(pair)

        if len(self.stimulation_action_pairs) > self.max_action_memory:
            LowestPoints = None
            for index, item in enumerate(self.stimulation_action_pairs):
                if LowestPoints == None:
                    LowestPoints = index
                else:
                    if item.points < self.stimulation_action_pairs[LowestPoints].points:
                        LowestPoints = index
            self.stimulation_action_pairs.pop(LowestPoints)
            

@dataclass
class Hand:
    state: str
    swing_dis: Optional[float] = 0.0
    swing_speed: Optional[float] = 0.0

    position: List[float] = field(
        default_factory=lambda: [0.0, 0.0]
    )

    owner_id: str = "default"


#Now this is the REAL BOXER!!!!! he has memory, Stamina and MentalClearness both Active and Avalible
#Avalible will be like the Max untill Hit where it will go down, Active will always regen to the Avalible level quickly but once it reaches Avalible it pushes Active and Avalible back up to max at a slower rate.
#That Avalible recovery is 4X slower then active
@dataclass
class Boxer:

    boxer_id: Optional[str] = None

    right_hand: Optional[Hand] = None
    left_hand: Optional[Hand] = None

    memory: Optional[Memory] = None

    active_stamina: Optional[float] = None
    available_stamina: Optional[float] = None
    max_stamina: Optional[float] = None

    active_mental_clearness: Optional[float] = None
    available_mental_clearness: Optional[float] = None
    max_mental_clearness: Optional[float] = None

    state: str = "Thinking"

    ticks_to_next_action: Optional[int] = 0

    body_radius: Optional[float] = None
    hands_radius: Optional[float] = None
    head_radius: Optional[float] = None

    current_executing_action_group: Optional[ActionGroup] = None

    position: Optional[List[float]] = field(
        default_factory=lambda: [0.0, 0.0]
    )
    head_position: Optional[List[float]] = field(
        default_factory=lambda: [0.0, 0.0]
    )

    rotation: Optional[float] = 0.0

    current_speed: Optional[List[float]] = field(
        default_factory=lambda: [0.0, 0.0]
    )
    max_speed: Optional[float] = 0.0
    friction: Optional[float] = 0.0

    def tick(self):
        if self.ticks_to_next_action <= 0:
            clarity_ratio = (
                self.active_mental_clearness / self.max_mental_clearness
                if self.max_mental_clearness > 0
                else 1.0
            )

            additional_ticks = round((1.0 - clarity_ratio) * 23)

            self.ticks_to_next_action += 14 + additional_ticks
        elif self.state == "Fighting":
            if self.ticks_to_next_action <= 4:
                self.ticks_to_next_action = 4
            else:
                self.ticks_to_next_action -= 1
        else:
            if self.ticks_to_next_action > 0:
                self.ticks_to_next_action -= 1
            else:
                self.state = "Action"
        
        self.update_postion()

    def rotate_body_parts(self):
        x, y = self.position

        #Head
        distance = 30
        rotation_rad = math.radians(self.rotation)
        dx = math.sin(rotation_rad) * distance
        dy = -math.cos(rotation_rad) * distance

        self.head_position = [x+dx, y+dy]

        #Hands
        forward_distance = 50
        side_distance = 50

        forward_rad = math.radians(self.rotation)
        right_rad = math.radians(self.rotation + 90)

        fxr = math.sin(forward_rad) * forward_distance + self.right_hand.swing_dis
        fyr = -math.cos(forward_rad) * forward_distance + self.right_hand.swing_dis
        fxl = math.sin(forward_rad) * forward_distance + self.left_hand.swing_dis 
        fyl = -math.cos(forward_rad) * forward_distance + self.left_hand.swing_dis

        rx = math.sin(right_rad) * side_distance
        ry = -math.cos(right_rad) * side_distance

        left_hand_position = [
            x + fxl - rx,
            y + fyl - ry
        ]

        right_hand_position = [
            x + fxr + rx,
            y + fyr + ry
        ]

        self.left_hand.position = left_hand_position

        self.right_hand.position = right_hand_position

    def update_postion(self):
        speed_x, speed_y = self.current_speed
        if speed_x == 0.0:
            speed_x = 0.0
        elif speed_x > 0 and speed_x < 2:
            speed_x = 0.0
        elif speed_x < 0 and speed_x > -2:
            speed_x = 0.0
        elif speed_x > 0:
            speed_x -= self.friction
        else:
            speed_x += self.friction
        
        if speed_y == 0.0:
            speed_y = 0.0
        elif speed_y > 0 and speed_y < 2:
            speed_y = 0.0
        elif speed_y < 0 and speed_y > -2:
            speed_y = 0.0
        elif speed_y > 0:
            speed_y -= self.friction
        else:
            speed_y += self.friction

        self.current_speed = [speed_x,speed_y]
        x, y = self.position
        self.position = [x+speed_x,y+speed_y]
        self.rotate_body_parts()

    def move(self, distance:float):
        rotation_rad = math.radians(self.rotation)
        dx = math.sin(rotation_rad) * distance
        dy = -math.cos(rotation_rad) * distance

        speed_x, speed_y = self.current_speed
        if speed_x + dx >= self.max_speed or speed_x + dx <= -self.max_speed:
            if speed_x > 0:
                speed_x = self.max_speed
            else:
                speed_x = -self.max_speed
        else:
            speed_x += dx
        
        if speed_y + dy >= self.max_speed or speed_y + dy <= -self.max_speed:
            if speed_y > 0:
                speed_y = self.max_speed
            else:
                speed_y = -self.max_speed
        else:
            speed_y += dy
        
        self.current_speed = [speed_x,speed_y]
        
    def rotate(self, amount: float):

        if self.rotation + amount > 360:
            self.rotation += amount - 360
        elif self.rotation + amount < 0:
            self.rotation += amount + 360
        elif self.rotation == 360:
            self.rotation = 0
        else:
            self.rotation += amount
        
        self.rotate_body_parts()

    def drain_stamina(self, amount: float):

        self.active_stamina -= amount

        if self.active_stamina < 0:
            self.active_stamina = 0
            self.available_stamina -= amount/1.5
            if self.available_stamina < 0:
                self.active_stamina = 0
                self.available_stamina = 0

    def recover_stamina(self, amount: float):

        if self.active_stamina < self.available_stamina:

            self.active_stamina += amount

            if self.active_stamina > self.available_stamina:
                if self.available_stamina > self.max_stamina:
                    self.available_stamina = self.max_stamina
                    self.active_stamina = self.available_stamina
                else:
                    self.available_stamina += amount/4
                    self.active_stamina = self.available_stamina

    def drain_mental(self, amount: float):

        self.active_mental_clearness -= amount

        if self.active_mental_clearness < 0:
            self.active_mental_clearness = 0
            self.available_mental_clearness -= amount/1.5
            if self.available_mental_clearness < 0:
                self.active_mental_clearness = 0
                self.available_mental_clearness = 0

    def recover_mental(self, amount: float):

        if self.active_mental_clearness < self.available_mental_clearness:

            self.active_mental_clearness += amount

            if self.active_mental_clearness > self.available_mental_clearness:
                if self.available_mental_clearness > self.max_stamina:
                    self.available_mental_clearness = self.max_stamina
                    self.active_mental_clearness = self.available_mental_clearness
                else:
                    self.available_mental_clearness += amount/4
                    self.active_mental_clearness = self.available_mental_clearness
