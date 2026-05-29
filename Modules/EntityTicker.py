from .Entityhandler import Entitys
from .Boxersmodules import ReuseFunctions
import time
import threading
from .EntityUpdater import Tick

CurrentTPS = ReuseFunctions.LoadSetting("Simulations defult TPS")
TimePerTick = 1.0 / CurrentTPS

StopEvent = threading.Event()

def UpdateTPS(TPS):
    global CurrentTPS, TimePerTick
    CurrentTPS = TPS
    TimePerTick = 1.0 / CurrentTPS

def Start():
    global CurrentTPS, TimePerTick
    while not StopEvent.is_set():
        for Entity in Entitys:
            Entity.tick()
        
        Tick()
        time.sleep(TimePerTick)