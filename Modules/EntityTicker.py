from .Entityhandler import Entitys
from .Boxersmodules import ReuseFunctions
import time
import threading

CurrentTPS = ReuseFunctions.LoadSetting("Simulations defult TPS")
TimePerTick = 1.0 / CurrentTPS

StopEvent = threading.Event()

def UpdateTPS(TPS):
    CurrentTPS = TPS
    TimePerTick = 1.0 / CurrentTPS

def Start():
    while not StopEvent.is_set():
        for Entity in Entitys:
            Entity.tick()
        
        time.sleep(TimePerTick)