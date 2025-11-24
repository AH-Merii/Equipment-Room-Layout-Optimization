import pytest
from floor import Floor
from room import Room


@pytest.fixture
def sample_floor():
    f = Floor(1)
    # A is adjacent to B, B is adjacent to C. A is NOT adjacent to C.
    r_a = Room("A", adjacent_rooms=["B"])
    r_b = Room("B", adjacent_rooms=["A", "C"])
    r_c = Room("C", adjacent_rooms=["B"])

    f.add_room(r_a)
    f.add_room(r_b)
    f.add_room(r_c)
    return f


def test_add_door_success(sample_floor):
    """Test adding a door between adjacent rooms."""
    sample_floor.add_door_between("A", "B")

    room_a = sample_floor.get_room("A")
    room_b = sample_floor.get_room("B")

    # Check door dictionaries
    assert "B" in room_a.doors.values()
    assert "A" in room_b.doors.values()


def test_add_door_failure_non_adjacent(sample_floor):
    """Test error when adding door between non-adjacent rooms."""
    with pytest.raises(ValueError, match="not adjacent"):
        sample_floor.add_door_between("A", "C")


def test_pathfinding(sample_floor):
    """Test finding path through connected doors."""
    # Connect A-B and B-C
    sample_floor.add_door_between("A", "B")
    sample_floor.add_door_between("B", "C")

    path = sample_floor.find_path("A", "C")
    assert path == ["A", "B", "C"]


def test_pathfinding_no_connection(sample_floor):
    """Test pathfinding when walls exist but no doors connect them."""
    # Only connect A-B. C is walled off.
    sample_floor.add_door_between("A", "B")

    path = sample_floor.find_path("A", "C")
    assert path == []
