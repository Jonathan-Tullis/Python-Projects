import dungeon_escape as game

def test_move_to_room():
    assert game.move_to_room("start", "Go Left") == "armory"
    assert game.move_to_room("start", "Go Right") == "beast_room"
    assert game.move_to_room("start", "Wrong") is None

def test_inventory_add_remove():
    inv = []
    game.add_to_inventory(inv, "key")
    assert "key" in inv

    game.remove_from_inventory(inv, "key")
    assert "key" not in inv

def test_pickup_logic():
    # Reset game state
    game.player_state["location"] = "hallway"
    game.player_state["inventory"] = []
    game.rooms["hallway"]["items"] = ["sword"]

    result1 = game.pick_up_item()
    assert "picked up the sword" in result1

    result2 = game.pick_up_item()
    assert result2 == "There's nothing to pick up."
