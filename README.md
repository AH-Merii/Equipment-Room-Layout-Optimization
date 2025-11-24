This repo contains the solutions to both given tasks.

## Equipment Layout Optimization Task

The solution for the equipment layout optimization task can be found in `equipment_layout_optimization.md`. I have also included a `brainstorming.md` file that contains, my raw thought process, it is a less refined version of the solution. You can use the commits to see how my ideas evolved over time.

## Building Data Representation Task

### Project Structure

The project is organized as a Python package (building_simulator) with a separate test suite.

```
├── building_simulator/ # Core Logic Package
│ ├── building.py # Main container class
│ ├── floor.py # Graph management & connectivity logic
│ ├── room.py # Node state (lights, windows, adjacency)
│ └── pathfind.py # BFS Algorithm implementation
├── tests/ # Test Suite (pytest)
│ ├── test_building.py
│ ├── test_floor.py
│ ├── test_pathfind.py
│ └── test_room.py
└── pyproject.toml # Dependencies (managed by uv)
```

### Design Approach

#### 1. Data Representation (The "What")

We modeled the building using a hierarchical composition pattern:

- **Building**: The top-level container holding a registry of floors.

- **Floor**: Acts as the Graph Container. It holds the registry of all rooms (Nodes) and manages the connections between them.

- **Room**: Acts as the Graph Node. It holds internal state (lights, windows) and an immutable list of physical neighbors (walls).

#### 2. Graph Representation (The "How")

We utilized an Adjacency List pattern to represent the floor plan:

- **Nodes**: Room objects.

- **Edges**: Represented by the doors dictionary inside each room.

* **Adjacency**: We distinguish between physical adjacency (sharing a wall) and traversability (having a door). A door cannot be created unless physical adjacency exists.

#### 3. Pathfinding Algorithm

Since the "cost" of moving between any two connected rooms is equal (1 step), we implemented Breadth-First Search (BFS).

- **Why BFS?** It guarantees the shortest path in an unweighted graph and is computationally efficient ($O(V+E)$) for sparse graphs like building layouts.

- **Separation of Concerns**: The algorithm lives in pathfind.py, decoupled from the Floor class logic.

### Usage

This project uses `uv` for fast dependency management.

**Installation**

Initialize the environment:

```
uv sync
```

**Running Tests**
The tests are automatically run on every commit pushed to the repo. To manually run the tests:

```
uv run pytest
```
