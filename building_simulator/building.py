from building_simulator.floor import Floor


class Building:
    """
    Represents the building containing floors.
    """

    def __init__(self, name: str):
        self.name = name
        self.floors: dict[int, Floor] = {}

    def add_floor(self, floor: Floor):
        self.floors[floor.floor_level] = floor

    def get_floor(self, level: int) -> Floor | None:
        return self.floors.get(level)

    def __repr__(self):
        return f"Building(Name: {self.name}, Floors: {list(self.floors.keys())})"
