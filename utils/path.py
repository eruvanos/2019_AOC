import math
from collections import deque
from typing import List

from utils import Vector
from utils.data import PriorityQueue


def manhattan(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def flip(pos):
    return pos[1], pos[0]


class Graph:
    def neighbors(self, current: Vector) -> List:
        raise NotImplementedError()

    def cost(self, current: Vector, next: Vector) -> int:
        raise NotImplementedError()


class GridGraph(Graph):
    def neighbors(self, current: Vector) -> List:
        raise NotImplementedError()

    def cost(self, current: Vector, next: Vector):
        return manhattan(current, next)


class ArrayGraph(GridGraph):
    """
    Graph implementation backed by an array like obj used like obj[x][y] -> bool

    Value:
    * True: blocked
    * False: free to go
    """

    def __init__(self, map):
        self._map = map

    def neighbors(self, current: Vector) -> List:
        x, y = current
        pos_neighbors = [
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)
        ]
        return [(x, y) for x, y in pos_neighbors if self._map[x][y]]


class MapGraph(GridGraph):
    """
    Graph implementation backed by a map used like map[(x,y)] -> bool

    Value:
    * True: blocked
    * False: free to go
    """

    def __init__(self, map):
        self._map = map

    def neighbors(self, current: Vector) -> List:
        x, y = current
        pos_neighbors = [
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)
        ]
        return [(x, y) for x, y in pos_neighbors if self._map[x][y]]


class SetGraph(GridGraph):
    """
    Graph implementation backed by a set used like pos in set -> bool

    Value:
    * True: blocked
    * False: free to go
    """

    def __init__(self, map):
        self._map = map

    def neighbors(self, current: Vector) -> List:
        x, y = current
        pos_neighbors = [
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)
        ]
        return [(x, y) for x, y in pos_neighbors if (x, y) not in self._map]


def reconstruct_path(came_from, goal):
    current = goal
    path = [current]
    while came_from[current]:
        current = came_from[current]
        path.append(current)
    path.reverse()  # optional
    return path[1:]


def a_star_search(graph: Graph, start, goal):
    if start == goal:
        return []

    # frontier = PriorityQueue()
    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from = {start: None}
    cost_so_far = {start: (0, None)}

    while not frontier.empty():
        current = frontier.get()[1]

        if current == goal:
            return reconstruct_path(came_from, goal)

        neighbors = graph.neighbors(current)
        for next in neighbors:
            new_cost = cost_so_far[current][0] + graph.cost(current, next)
            if (next not in cost_so_far or (new_cost, flip(current)) < cost_so_far[next]):
                cost_so_far[next] = (new_cost, flip(current))
                priority = new_cost + manhattan(goal, next)

                frontier.put((priority, next))
                came_from[next] = current

    # return came_from, cost_so_far
    return None


def deepsearch(graph: Graph, pos, targets):
    if pos in targets:
        return []

    todo = deque()
    came_from = {pos: None}

    todo.append((0, pos))

    found = []
    max_depth = math.inf
    while todo:
        depth, current = todo.popleft()
        if max_depth < depth:
            break

        neighbors = graph.neighbors(current)
        for neighbor in neighbors:
            if neighbor not in came_from:
                todo.append((depth + 1, neighbor))
                came_from[neighbor] = current

                if neighbor in targets:
                    max_depth = min(depth, max_depth)
                    found.append(neighbor)

    if len(found) == 0:
        return None

    found.sort(key=lambda p: flip(p))
    return reconstruct_path(came_from, found[0])
