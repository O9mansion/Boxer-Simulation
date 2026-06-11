import Modules.Renderer as Renderer
import Modules.Ring as Ring
import Modules.Entityhandler as EntityHandler
import threading
import Modules.EntityUpdater as EntityUpdater
import Modules.EntityTicker as EntityTicker

Ring.Setup()
EntityUpdater.Setup()

def Test():
    EntityUpdater.Test("Rotation And Moving")

def StartTicking():
    EntityTicker.Start()

t1 = threading.Thread(target=Test)
t1.start()

t2 = threading.Thread(target=StartTicking)
t2.start()

try:
    Renderer.Start([800, 800])
finally:
    EntityTicker.StopEvent.set()
    t2.join
    print("Shutdown")

