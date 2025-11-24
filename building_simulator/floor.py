from building_simulator.pathfind import find_shortest_path_bfs
from building_simulator.room import Room


class Floor:
    """
    Represents a floor containing multiple rooms.
    Handles graph operations like adding doors and pathfinding.
    """

    def __init__(self, floor_level: int):
        self.floor_level = floor_level
        self.rooms: dict[str, Room] = {}

    def add_room(self, room: Room):
        self.rooms[room.name] = room

    def get_room(self, room_name: str) -> Room | None:
        return self.rooms.get(room_name)

    def add_door_between(self, room_name_a: str, room_name_b: str):
        """
        Adds a door between room A and room B if they are physically adjacent.
        """
        room_a = self.get_room(room_name_a)
        room_b = self.get_room(room_name_b)

        if not room_a or not room_b:
            raise ValueError("One or both rooms do not exist on this floor.")

        # Check adjacency (Physical walls must exist to put a door)
        if not room_a.is_adjacent(room_name_b) or not room_b.is_adjacent(room_name_a):
            raise ValueError(
                f"Cannot add door: {room_name_a} and {room_name_b} are not adjacent."
            )

        # Add door to A pointing to B
        room_a.add_door_connection(room_name_b)
        # Add door to B pointing to A
        room_b.add_door_connection(room_name_a)

    def find_path(self, start_room_name: str, end_room_name: str) -> list[str]:
        """
        Delegates to the external pathfinding module.
        """
        return find_shortest_path_bfs(self.rooms, start_room_name, end_room_name)

    def __repr__(self):
        return f"Floor(Level: {self.floor_level}, Rooms: {list(self.rooms.keys())})"
