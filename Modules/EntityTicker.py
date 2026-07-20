from .Entityhandler import Entitys, Update
from .Boxersmodules import ReuseFunctions
import time
import threading
from .EntityUpdater import Tick

CurrentTPS = ReuseFunctions.LoadSetting("Simulations defult TPS")
print(CurrentTPS)
TimePerTick = 1.0 / CurrentTPS

StopEvent = threading.Event()

def UpdateTPS(TPS):
    global CurrentTPS, TimePerTick
    CurrentTPS = TPS
    TimePerTick = 1.0 / CurrentTPS

def Start():
    global CurrentTPS, TimePerTick
    Update()
    while not StopEvent.is_set():
        for Entity in Entitys:
            Entity.tick()
        
        Tick()
        Update()
        time.sleep(TimePerTick)