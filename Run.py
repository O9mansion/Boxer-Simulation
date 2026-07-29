import Modules.Renderer as Renderer
import Modules.Ring as Ring
import Modules.Entityhandler as EntityHandler
import threading
import Modules.EntityUpdater as EntityUpdater
import Modules.EntityTicker as EntityTicker
import Modules.Boxersmodules.ReuseFunctions as ReuseFunctions

Ring.Setup()
EntityUpdater.Setup()

def Test():
    EntityUpdater.Test("Movement")

def StartTicking():
    EntityTicker.Start()

t1 = threading.Thread(target=Test)
t1.start()

t2 = threading.Thread(target=StartTicking)
t2.start()

ScreenX = ReuseFunctions.LoadSetting("Screen Size X")
ScreenY = ReuseFunctions.LoadSetting("Screen Size Y")

try:
    Renderer.Start([ScreenX, ScreenY])
finally:
    EntityTicker.StopEvent.set()
    t2.join
    print("Shutdown")

