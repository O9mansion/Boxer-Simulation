import Run


def test_main_runs_test_before_starting_tick_loop(monkeypatch):
    events = []

    class FakeThread:
        def __init__(self, target, daemon=False):
            self.target = target

        def start(self):
            self.target()

        def join(self, timeout=None):
            pass

    class DummyEvent:
        def set(self):
            events.append("stop")

    monkeypatch.setattr(Run.Ring, "Setup", lambda: events.append("ring"))
    monkeypatch.setattr(Run.EntityUpdater, "Setup", lambda: events.append("setup"))
    monkeypatch.setattr(Run.EntityUpdater, "Test", lambda kind: events.append(("test", kind)))
    monkeypatch.setattr(Run.EntityTicker, "Start", lambda: events.append("tick"))
    monkeypatch.setattr(Run.EntityTicker, "StopEvent", DummyEvent())
    monkeypatch.setattr(Run.Renderer, "Start", lambda size: events.append(("render", size)))
    monkeypatch.setattr(Run.threading, "Thread", FakeThread)
    monkeypatch.setattr(Run.ReuseFunctions, "LoadSetting", lambda name: 800 if name == "Screen Size X" else 600)

    Run.main()

    assert events[:4] == ["ring", "setup", ("test", "HeadBodyHand"), "tick"]
