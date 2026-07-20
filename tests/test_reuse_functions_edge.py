import math
from Modules.Boxersmodules import ReuseFunctions as RF
from Modules.classes import Stimulation, Memory, StimulationActionPair


def test_returned_flipped_situation_angles():
    s = Stimulation()
    s.angle_to_opponent = 10
    s.angle_to_ring_center = 200
    s.relative_opponent_angle = 45
    s.self_rotation_speed = 1.2
    s.opponent_rotation_speed = -0.5
    s.closing_speed = 0.3
    s.distance_to_opponent = 5
    s.distance_to_ring_center = 6

    f = RF.ReturnedFlippedSituation(s)
    assert f.flipped is True
    assert math.isclose(f.angle_to_opponent, RF.FlipRotaion(10))
    assert math.isclose(f.angle_to_ring_center, RF.FlipRotaion(200))
    assert math.isclose(f.relative_opponent_angle, RF.FlipRotaion(45))
    assert f.self_rotation_speed == s.self_rotation_speed


def test_compare_two_stimulations_symmetric():
    a = Stimulation()
    b = Stimulation()
    a.angle_to_opponent = 10
    b.angle_to_opponent = 20
    diff1 = RF.CompareTwoStimulations(a, b)
    diff2 = RF.CompareTwoStimulations(b, a)
    assert math.isclose(diff1, diff2)
    assert diff1 >= 0


def test_return_best_situation_with_flip_and_memory():
    mem = Memory(max_action_memory=4)
    s1 = Stimulation()
    s1.angle_to_opponent = 10
    pair = StimulationActionPair(stimulation=s1, action=None, points=1)
    mem.stimulation_action_pairs.append(pair)

    query = Stimulation()
    query.angle_to_opponent = 10

    idx, diff, flipped = RF.ReturnBestSituationBasedOnStimuli(query, mem)
    assert diff >= 0
    assert idx is not None


def test_resolve_collision_separates_but_no_impulse_when_moving_apart():
    from Modules.classes import Boxer

    b1 = Boxer()
    b2 = Boxer()
    b1.position = [0.0, 0.0]
    b2.position = [1.0, 0.0]
    b1.current_speed = [0.0, 0.0]
    b2.current_speed = [10.0, 0.0]
    # Use large radii to force overlap
    collision = RF.CirclesCollitionCheck(b1.position, 5, b2.position, 5)

    old_speeds = (b1.current_speed.copy(), b2.current_speed.copy())
    old_positions = (b1.position.copy(), b2.position.copy())

    RF.ResolveCollision(b1, b2, collision)

    # Positions should have been corrected
    assert b1.position != old_positions[0] or b2.position != old_positions[1]
    # But speeds remain unchanged because they were moving apart
    assert b1.current_speed == old_speeds[0]
    assert b2.current_speed == old_speeds[1]


def test_resolve_collision_applies_impulse_when_moving_towards():
    from Modules.classes import Boxer
    from Modules.classes import Hand

    b1 = Boxer()
    b2 = Boxer()
    # Ensure hands exist so rotate_body_parts doesn't fail
    b1.right_hand = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0,0], owner_id="1")
    b1.left_hand = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0,0], owner_id="1")
    b2.right_hand = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0,0], owner_id="2")
    b2.left_hand = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0,0], owner_id="2")
    b1.position = [0.0, 0.0]
    b2.position = [1.0, 0.0]
    b1.current_speed = [5.0, 0.0]
    b2.current_speed = [-5.0, 0.0]
    collision = RF.CirclesCollitionCheck(b1.position, 5, b2.position, 5)

    old_speeds = (b1.current_speed.copy(), b2.current_speed.copy())
    RF.ResolveCollision(b1, b2, collision)

    # After collision, speeds should have changed
    assert b1.current_speed != old_speeds[0] or b2.current_speed != old_speeds[1]
