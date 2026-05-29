import tkinter as tk
import Modules.classes as Classes
import Modules.Entityhandler as EntityHandler
import math

root = tk.Tk()
canvas = None

root.title("Simulation")

def StartingCondidtions(WorldSize):
    global canvas

    canvas = tk.Canvas(
        root,
        width=WorldSize[0],
        height=WorldSize[1],
        bg="#2f3b4f"
    )

    canvas.pack()

def DrawBoxer(Boxer: Classes.Boxer):
    global canvas

    x, y = Boxer.position

    body_radius = Boxer.body_radius

    body_left = x - body_radius
    body_top = y - body_radius
    body_right = x + body_radius
    body_bottom = y + body_radius

    #Body
    canvas.create_oval(
        body_left,
        body_top,
        body_right,
        body_bottom,
        fill="#f6f7df",
        outline="black",
        width=2
    )

    head_x, head_y = Boxer.head_position
    head_radius = Boxer.head_radius

    head_left = head_x - head_radius
    head_top = head_y - head_radius
    head_right = head_x + head_radius
    head_bottom = head_y + head_radius

    canvas.create_oval(
        head_left,
        head_top,
        head_right,
        head_bottom,
        fill="#f6f7df",
        outline="black",
        width=2
    )

    # Hands
    hand_radius = Boxer.hands_radius
    right_x,right_y = Boxer.right_hand.position
    left_x,left_y = Boxer.left_hand.position

    left_left = left_x - hand_radius
    left_top = left_y - hand_radius
    left_right = left_x + hand_radius
    left_bottom = left_y + hand_radius

    right_left = right_x - hand_radius
    right_top = right_y - hand_radius
    right_right = right_x + hand_radius
    right_bottom = right_y + hand_radius

    canvas.create_oval(
        left_left,
        left_top,
        left_right,
        left_bottom,
        fill="#f6f7df",
        outline="black",
        width=2
    )

    canvas.create_oval(
        right_left,
        right_top,
        right_right,
        right_bottom,
        fill="#f6f7df",
        outline="black",
        width=2
    )



def Update():
    global canvas

    # Clear previous frame
    canvas.delete("all")

    # Draw arena
    canvas.create_oval(
        50,
        50,
        750,
        750,
        fill="#434d5f",
        outline="#636d80",
        width=5
    )

    # Draw all boxers
    for boxer in EntityHandler.Entitys:
        DrawBoxer(boxer)

    # Schedule next frame
    root.after(16, Update)  # ~60 FPS

def Start(WorldSize):
    StartingCondidtions(WorldSize)

    Update()

    root.mainloop()