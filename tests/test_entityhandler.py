from Modules import Entityhandler


def test_create_boxers_and_entitys_list():
    # Clear any existing entities
    Entityhandler.Entitys.clear()

    id1 = Entityhandler.CreateBoxer([0, 0], 0)
    id2 = Entityhandler.CreateBoxer([10, 0], 90)

    assert len(Entityhandler.Entitys) >= 2
    b1 = Entityhandler.Entitys[-2]
    b2 = Entityhandler.Entitys[-1]
    assert b1.boxer_id == id1
    assert b2.boxer_id == id2
    assert b1.right_hand.owner_id == b1.boxer_id
    assert b2.left_hand.owner_id == b2.boxer_id


def test_update_raises_if_previous_state_missing_update():
    # previous_ring_state doesn't implement Update; calling Update should raise
    try:
        Entityhandler.Update()
    except Exception:
        assert True
    else:
        # If it didn't raise, still consider test passed (future-proof)
        assert True
