"""
You and the elephants finally reach fresh air. You've emerged near the base of a large volcano that seems to be actively erupting! Fortunately, the lava seems to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the cavern exit a little longer. Outside the cave, you can see the lava landing in a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools, it might be forming obsidian! The cooling rate should be based on the surface area of the lava droplets, so you take a quick scan of a droplet as it flies past you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its resolution is quite low and, as a result, it approximates the shape of the lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube. So, if your scan were only two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
In the above example, after counting up all the sides that aren't connected to another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?
"""

import re
from collections import deque

import networkx as nx

points = set()

with open("input.txt", "r") as f:

    digit = r"\d+"

    for line in f:
        points.add(tuple(map(int, re.findall(digit, line))))

outside_points = set()
inside_points = set()


def is_outside(x, y, z, part):

    if (x, y, z) in outside_points:
        return True
    if (x, y, z) in inside_points:
        return False

    seen_points = set()
    queue = deque([(x, y, z)])

    while queue:
        x, y, z = queue.popleft()

        if (x, y, z) in points or (x, y, z) in seen_points:
            continue

        seen_points.add((x, y, z))

        # Check if the point is inside the cavity in part 2
        if len(seen_points) > (10000 if part == 2 else 0):
            for point in seen_points:
                outside_points.add(point)
            return True

        queue.append((x - 1, y, z))
        queue.append((x + 1, y, z))
        queue.append((x, y - 1, z))
        queue.append((x, y + 1, z))
        queue.append((x, y, z - 1))
        queue.append((x, y, z + 1))

    for point in seen_points:
        inside_points.add(point)

    return False


surface_area = 0

for x, y, z in points:
    if is_outside(x - 1, y, z, 1):
        surface_area += 1
    if is_outside(x + 1, y, z, 1):
        surface_area += 1
    if is_outside(x, y - 1, z, 1):
        surface_area += 1
    if is_outside(x, y + 1, z, 1):
        surface_area += 1
    if is_outside(x, y, z - 1, 1):
        surface_area += 1
    if is_outside(x, y, z + 1, 1):
        surface_area += 1

# Part 1
print(surface_area)

"""
Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?
"""

outside_points = set()
inside_points = set()
surface_area = 0

for x, y, z in points:
    if is_outside(x - 1, y, z, 2):
        surface_area += 1
    if is_outside(x + 1, y, z, 2):
        surface_area += 1
    if is_outside(x, y - 1, z, 2):
        surface_area += 1
    if is_outside(x, y + 1, z, 2):
        surface_area += 1
    if is_outside(x, y, z - 1, 2):
        surface_area += 1
    if is_outside(x, y, z + 1, 2):
        surface_area += 1

# Part 2
print(surface_area)
