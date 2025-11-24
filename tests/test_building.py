from building_simulator.building import Building
from building_simulator.floor import Floor


def test_building_hierarchy():
    b = Building("Skyscraper")
    f1 = Floor(1)
    b.add_floor(f1)
    assert b.get_floor(1) == f1
    assert b.get_floor(99) is None


def test_building_name():
    b = Building("My House")
    assert b.name == "My House"


def test_empty_building():
    b = Building("Empty Lot")
    assert len(b.floors) == 0
