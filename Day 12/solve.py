"""
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

import math

with open("input.txt") as f:
    data = f.read().splitlines()


class Node:

    convert_elevation = {
        chr(i): i - ord("a") + 1 for i in range(ord("a"), ord("z") + 1)
    }

    def __init__(self, elevation):

        self.char = elevation
        self.__set_elevation(elevation)
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def __set_elevation(self, elevation):

        if elevation == "S":
            self.elevation = 1
        elif elevation == "E":
            self.elevation = 26
        else:
            self.elevation = self.convert_elevation[elevation]

    def __str__(self):
        return f"Node with elevation: {self.elevation}"


class Graph:
    def __init__(self):

        self.nodes = []

    def from_map(self, map):

        for i, row in enumerate(map):
            for j, node in enumerate(row):
                self.nodes.append(node)

                if i > 0:
                    node.add_neighbor(map[i - 1][j])
                    map[i - 1][j].add_neighbor(node)
                if j > 0:
                    node.add_neighbor(map[i][j - 1])
                    map[i][j - 1].add_neighbor(node)
                if i < len(map) - 1:
                    node.add_neighbor(map[i + 1][j])
                    map[i + 1][j].add_neighbor(node)
                if j < len(row) - 1:
                    node.add_neighbor(map[i][j + 1])
                    map[i][j + 1].add_neighbor(node)

    def bfs(self, start: Node, end: Node):

        queue = [start]
        visited = set()
        visited.add(start)
        path = {start: None}

        while queue:
            current = queue.pop(0)
            if current == end:
                break
            for neighbor in current.neighbors:
                if (
                    neighbor not in visited
                    and neighbor.elevation - current.elevation <= 1
                    and neighbor.elevation != 1
                ):
                    visited.add(neighbor)
                    queue.append(neighbor)
                    path[neighbor] = current

        current = end
        path_list = [current]
        while current != start:
            if current not in path:
                return math.inf
            current = path[current]
            path_list.append(current)

        return len(path_list) - 1

    def __str__(self):
        return f"Nodes: {len(self.nodes)}"


map = []
start_node = None
end_node = None

for line in data:
    map.append([])
    for char in line:
        map[-1].append(Node(char))

        if char == "S":
            start_node = map[-1][-1]
        elif char == "E":
            end_node = map[-1][-1]

g = Graph()
g.from_map(map)

path = g.bfs(start_node, end_node)

# Part 1
print(path)

"""
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
"""

possible_starts = [node for node in g.nodes if node.elevation == 1]

shortest_path = math.inf

for possible_start in possible_starts:
    path = g.bfs(possible_start, end_node)
    if path < shortest_path:
        shortest_path = path

# Part 2
print(shortest_path)
