from .Entityhandler import Entitys, Update
from .Boxersmodules import ReuseFunctions
import time
import threading
from .EntityUpdater import Tick

CurrentTPS = ReuseFunctions.LoadSetting("Simulations defult TPS")
print(CurrentTPS)
TimePerTick = 1.0 / CurrentTPS
next_tick = time.perf_counter()

StopEvent = threading.Event()
Paused = False

def UpdateTPS(TPS):
    global CurrentTPS, TimePerTick
    CurrentTPS = TPS
    TimePerTick = 1.0 / CurrentTPS

def Pause():
    global Paused
    Paused = True

def Play():
    global Paused
    Paused = False

def Start():
    global CurrentTPS, TimePerTick
    Update()

    while not StopEvent.is_set():
        if Paused:
            time.sleep(sleep_time)
            continue

        next_tick += TimePerTick

        for entity in Entitys:
            entity.tick()

        Tick()
        Update()

        sleep_time = next_tick - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)