from Modules.classes import (
    ActionGroup,
    Boxer,
    Hand,
    Memory,
    Stimulation,
    StimulationActionPair,
)


def make_boxer_template():
    right = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0.0, 0.0], owner_id="r")
    left = Hand(state="Idle", swing_dis=0.0, swing_speed=0.0, position=[0.0, 0.0], owner_id="l")

    b = Boxer(
        boxer_id="test",
        right_hand=right,
        left_hand=left,
        max_puntching_distance=10,
        puntching_ierations=2,
        puntching_distance_growth_factor=2,
        puntching_returning_speed=1,
        memory=None,
        active_stamina=50,
        available_stamina=50,
        max_stamina=100,
        active_mental_clearness=20,
        available_mental_clearness=30,
        max_mental_clearness=100,
        state="Thinking",
        ticks_to_next_action=0,
        body_radius=10,
        hands_radius=2,
        head_radius=3,
        position=[0.0, 0.0],
        head_position=[0.0, 0.0],
        rotation=359,
        current_speed=[1.0, 1.0],
        max_speed=5,
        current_rotation_speed=5,
        max_rotation_speed=10,
        friction=1.0,
    )
    return b


def test_tick_sets_ticks_and_state_transitions():
    b = make_boxer_template()
    b.ticks_to_next_action = -1
    b.max_mental_clearness = 100
    b.active_mental_clearness = 50
    b.tick()
    assert b.ticks_to_next_action >= 14

    b.state = "Fighting"
    b.ticks_to_next_action = 2
    b.tick()
    assert b.ticks_to_next_action == 4


def test_rotation_wrapping_and_friction_effects():
    b = make_boxer_template()
    b.current_rotation_speed = 5
    b.rotation = 359
    b.update_postion()
    assert 0 <= b.rotation <= 360


def test_stamina_and_mental_drain_and_recover():
    b = make_boxer_template()
    b.active_stamina = 5
    b.available_stamina = 5
    b.drain_stamina(10)
    assert b.active_stamina == 0
    assert b.available_stamina <= 5

    b.active_mental_clearness = 0
    b.available_mental_clearness = 2
    b.recover_mental(5)
    assert b.active_mental_clearness >= 0


def test_rotate_clamps_to_max():
    b = make_boxer_template()
    b.current_rotation_speed = 0
    b.rotate(100)
    assert abs(b.current_rotation_speed) <= b.max_rotation_speed


def test_recover_mental_caps_at_max_mental_clearness():
    b = make_boxer_template()
    b.active_mental_clearness = 90
    b.available_mental_clearness = 90
    b.max_mental_clearness = 80

    b.recover_mental(10)

    assert b.available_mental_clearness == 80
    assert b.active_mental_clearness == 80


def test_add_memory_prunes_lowest_points_when_limit_reached():
    memory = Memory(max_action_memory=2)
    pair_low = StimulationActionPair(
        stimulation=Stimulation(),
        action=ActionGroup(),
        points=1.0,
    )
    pair_mid = StimulationActionPair(
        stimulation=Stimulation(),
        action=ActionGroup(),
        points=2.0,
    )
    pair_high = StimulationActionPair(
        stimulation=Stimulation(),
        action=ActionGroup(),
        points=3.0,
    )

    memory.add_memory(pair_low)
    memory.add_memory(pair_mid)
    memory.add_memory(pair_high)

    assert len(memory.stimulation_action_pairs) == 2
    assert {pair.points for pair in memory.stimulation_action_pairs} == {2.0, 3.0}
