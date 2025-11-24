from room import Room


def test_room_initialization():
    """Test basic creation and immutability of adjacency list."""
    adj = ["Kitchen", "Hall"]
    r = Room("Living Room", adj, windows=2, lights=1)

    assert r.name == "Living Room"
    assert isinstance(r._adjacent_rooms, tuple)
    assert "Kitchen" in r._adjacent_rooms
    assert r.windows == 2


def test_room_attribute_modification():
    """Test add/remove/set methods for lights and windows."""
    r = Room("Test", [], windows=5, lights=5)

    # Windows
    r.add_windows(2)
    assert r.windows == 7
    r.remove_windows(10)  # Should stop at 0
    assert r.windows == 0
    r.set_windows(3)
    assert r.windows == 3

    # Lights
    r.add_lights(1)
    assert r.lights == 6
    r.set_lights(2)
    assert r.lights == 2


def test_adjacency_check():
    r = Room("A", ["B"])
    assert r.is_adjacent("B") is True
    assert r.is_adjacent("C") is False
