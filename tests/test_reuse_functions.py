import math
from Modules.Boxersmodules import ReuseFunctions as RF
from Modules.classes import Stimulation


def test_flip_rotation():
    assert RF.FlipRotaion(0) == 180
    assert RF.FlipRotaion(190) == 350


def test_distance_check():
    assert RF.DistanceCheckCircles([0, 0], [3, 4]) == 5


def test_circles_collision_no_overlap():
    collided, overlap, angle = RF.CirclesCollitionCheck([0, 0], 1, [10, 0], 1)
    assert collided is False
    assert overlap < 0


def test_circles_collision_overlap():
    collided, overlap, angle = RF.CirclesCollitionCheck([0, 0], 5, [3, 0], 5)
    assert collided is True
    assert overlap > 0
    assert isinstance(angle, float)


def test_make_object_id_increment():
    a = RF.MakeObjectID()
    b = RF.MakeObjectID()
    assert isinstance(a, int)
    assert b == a + 1


def test_return_thinking_time():
    val = RF.ReturnThinkingTime(10, 5)
    assert isinstance(val, (int, float))
    min_t = RF.LoadSetting("Minimum thinking time")
    max_t = RF.LoadSetting("Maximum thinking time")
    expected = min_t - ((5 / 10) * (min_t - max_t))
    assert math.isclose(val, expected, rel_tol=1e-6)
