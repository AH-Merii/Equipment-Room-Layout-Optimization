class Room:
    """
    Represents a single room in the building.
    Handles internal state like lights, windows, and door connections.
    """

    def __init__(
        self, name: str, adjacent_rooms: list[str], windows: int = 0, lights: int = 0
    ):
        self.name = name
        # Immutable tuple of physically adjacent rooms (walls)
        self._adjacent_rooms: tuple[str, ...] = tuple(adjacent_rooms)

        self.windows = windows
        self.lights = lights

        # Mapping: Door ID (int) -> Connected Room Name (str)
        self.doors: dict[int, str] = {}
        self._next_door_id = 1

    def is_adjacent(self, room_name: str) -> bool:
        """Checks if a specific room name is in the immutable adjacency list."""
        return room_name in self._adjacent_rooms

    def add_door_connection(self, target_room_name: str):
        """
        Internal method to add a door.
        Validation happens in the Floor class.
        """
        self.doors[self._next_door_id] = target_room_name
        self._next_door_id += 1

    def set_windows(self, count: int):
        self.windows = count

    def add_windows(self, count: int):
        self.windows += count

    def remove_windows(self, count: int):
        self.windows = max(0, self.windows - count)

    def set_lights(self, count: int):
        self.lights = count

    def add_lights(self, count: int):
        self.lights += count

    def remove_lights(self, count: int):
        self.lights = max(0, self.lights - count)

    def __repr__(self):
        return (
            f"Room(Name: {self.name}, Windows: {self.windows}, "
            f"Lights: {self.lights}, Doors to: {list(self.doors.values())})"
        )
