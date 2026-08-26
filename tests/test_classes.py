from Modules.classes import Boxer, Hand


def make_boxer():
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
        active_stamina=100,
        available_stamina=100,
        max_stamina=100,
        active_mental_clearness=50,
        available_mental_clearness=50,
        max_mental_clearness=100,
        state="Thinking",
        ticks_to_next_action=0,
        body_radius=10,
        hands_radius=2,
        head_radius=3,
        position=[0.0, 0.0],
        head_position=[0.0, 0.0],
        rotation=0,
        current_speed=[0.0, 0.0],
        max_speed=100,
        current_rotation_speed=0,
        max_rotation_speed=10,
        friction=0.5,
    )

    return b


def test_puntch_sets_hand_to_swinging():
    b = make_boxer()
    assert b.right_hand.state == "Idle"
    b.puntch("R")
    assert b.right_hand.state == "Swinging"


def test_update_hands_initial_growth():
    b = make_boxer()
    b.right_hand.state = "Swinging"
    b.right_hand.swing_dis = 0
    b.update_hands()
    assert b.right_hand.swing_dis > 0


def test_swing_reaches_full_extension_in_configured_steps():
    b = make_boxer()
    b.max_puntching_distance = 75
    b.puntching_ierations = 5
    b.puntching_distance_growth_factor = 2
    b.hand_air_time = 0
    b.right_hand.state = "Swinging"
    b.right_hand.swing_dis = 0

    for _ in range(5):
        b.update_hands()

    assert b.right_hand.swing_dis == 75
    assert b.right_hand.state == "Returning"

# Whatever I want
def test_move_updates_speed():
    b = make_boxer()
    b.rotation = 0
    b.current_speed = [0.0, 0.0]
    b.move(10)
    assert b.current_speed != [0.0, 0.0]
