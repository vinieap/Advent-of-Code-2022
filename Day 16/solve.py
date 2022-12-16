# Day       Time  Rank  Score       Time  Rank  Score
#  16   01:29:18  1219      0   01:39:21   336      0


import math
import re
from collections import defaultdict
from functools import cache

REGEX = r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w ,]+)$"

valves = {}
dist = defaultdict(lambda: defaultdict(lambda: math.inf))

for i, flow_rate, tunnels in re.findall(REGEX, open("input.txt").read(), re.MULTILINE):
    valves[i] = int(flow_rate)
    dist[i][i] = 0
    for j in tunnels.split(", "):
        dist[i][j] = 1

for k in valves:
    for i in valves:
        for j in valves:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])


def calculate_max_flow(minutes: int, part_2: bool):
    @cache
    def dp(i: str, t: int, remaining: frozenset, elephant: bool):
        ans = dp("AA", minutes, remaining, False) if elephant else 0
        for j in remaining:
            if (next_t := t - dist[i][j] - 1) >= 0:
                ans = max(
                    ans, valves[j] * next_t + dp(j, next_t, remaining - {j}, elephant)
                )
        return ans

    return dp("AA", minutes, frozenset(x for x in valves if valves[x] > 0), part_2)


# Part 1
print(calculate_max_flow(30, False))

"""
You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
With the elephant helping, after 26 minutes, the best you could do would release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most pressure you could release?
"""

# Part 2
print(calculate_max_flow(26, True))
