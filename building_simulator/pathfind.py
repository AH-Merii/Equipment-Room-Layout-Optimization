from collections import deque

from building_simulator.room import Room


def find_shortest_path_bfs(
    rooms: dict[str, Room], start_name: str, end_name: str
) -> list[str]:
    """
    Performs a Breadth-First Search (BFS) to find the shortest path
    between two rooms using the 'doors' graph connections.

    Args:
        rooms: A dictionary mapping room names to Room objects.
        start_name: The name of the starting room.
        end_name: The name of the destination room.

    Returns:
        A list of strings representing the path (e.g., ['A', 'B', 'C']).
        Returns an empty list if no path is found or rooms don't exist.
    """
    if start_name not in rooms or end_name not in rooms:
        return []

    # Queue holds: [current_room_name, [path_so_far]]
    queue = deque([(start_name, [start_name])])
    visited = {start_name}

    while queue:
        current_name, path = queue.popleft()
        current_room = rooms[current_name]

        if current_name == end_name:
            return path

        # Iterate through doors (the graph edges)
        for connected_room_name in current_room.doors.values():
            if connected_room_name not in visited:
                visited.add(connected_room_name)
                new_path = list(path)
                new_path.append(connected_room_name)
                queue.append((connected_room_name, new_path))

    return []
