""" This module implements Dijkstra's path planning algorithm.

Two variants are included: grid-based, and mesh-based.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Mario Cobos Maestre"
__authors__ = ["Mario Cobos Maestre"]
__contact__ = "mario.cobos@edu.uah.es"
__copyright__ = "Copyright 2019, UAH"
__credits__ = ["Mario Cobos Maestre"]
__date__ = "2019/03/29"
__deprecated__ = False
__email__ =  "mario.cobos@edu.uah.es"
__license__ = "GPLv3"
__maintainer__ = "Mario Cobos Maestre"
__status__ = "Development"
__version__ = "0.0.1"


from collections import deque

import path_planning as pp

def neighbors(point,grid):
    """
        Generates the list of neighbors for a given node located
        in a grid.
        Inputs:
            - point: node for which to generate those neighbors
            - grid: grid over which to operate.
        Outputs:
            - generated list of neighbors
    """
    x,y = point.grid_point
    if x > 0 and x < len(grid) - 1:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y),\
                      (x-1, y-1), (x-1, y+1), (x+1, y-1),\
                      (x+1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x+1,y),\
                      (x-1, y-1), (x+1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y + 1),(x+1,y),\
                      (x-1, y+1), (x+1, y+1)]]
    elif x > 0:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x,y + 1),\
                      (x-1, y-1), (x-1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x-1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y), (x,y + 1), (x-1, y+1)]]
    else:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y),(x,y - 1),(x,y + 1),\
                      (x+1, y-1), (x+1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y),(x,y - 1),(x+1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y), (x,y + 1), (x+1, y+1)]]
    return [link for link in links if link.value != 9]

def search_dijkstra(origin, goal, grid, heur=None, scale=None):
    """
        Executes the Dijkstra path planning algorithm over a grid.
        Inputs:
            - origin: node at which to start.
            - goal: node that needs to be reached.
            - grid: grid over which to perform the algorithm.
            - heur: reference to a string representing an heuristic.
            - scale: scale factor for the heuristic.
            Unused, kept to standarize input.
        Outputs:
            - ordered list of nodes representing the path found from
            origin to goal.
    """
    flatten = lambda l: [item for sublist in l for item in sublist]
    dist = {v: float('inf') for v in  flatten(grid)}
    previous = {v: None for v in flatten(grid)}
    dist[origin] = 0
    q = flatten(grid).copy()
    for m in q:
        for n in neighbors(m, grid):
            m.neighbors[n.point] = n

    while q:
        u = min(q, key=lambda v: dist[v])
        pp.expanded_nodes += 1
        q.remove(u)
        if dist[u] == float('inf') or u == goal:
            break
        for v in u.neighbors.values():
            alt = dist[u] + u.move_cost(v)
            if alt < dist[v]:
                dist[v] = alt
                previous[v] = u

    s, u = deque(), goal
    while previous[u]:
        s.appendleft(u)
        u = previous[u]
    s.appendleft(u)
    return s

pp.register_search_method('Dijkstra', search_dijkstra)

def search_dijkstra_mesh(origin, goal, mesh, heur=None, scale=None):
    """
        Executes the Dijkstra path planning algorithm over a mesh.
        Inputs:
            - origin: node at which to start.
            - goal: node that needs to be reached.
            - mesh: mesh over which to perform the algorithm.
            - heur: reference to a string representing an heuristic.
            - scale: scale factor for the heuristic.
            Unused, kept to standarize input.
        Outputs:
            - ordered list of nodes representing the path found from
            origin to goal.
    """
    dist = {v: float('inf') for v in  mesh.values()}
    previous = {v: None for v in mesh.values()}
    dist[origin] = 0
    q = list(mesh.values())

    while q:
        u = min(q, key=lambda v: dist[v])
        pp.expanded_nodes += 1
        q.remove(u)
        if dist[u] == float('inf') or u == goal:
            break
        for v in u.neighbors.values():
            alt = dist[u] + u.value
            if alt < dist[v]:
                dist[v] = alt
                previous[v] = u

    s, u = deque(), goal
    while previous[u]:
        s.appendleft(u)
        u = previous[u]
    s.appendleft(u)
    return s

pp.register_search_method('Dijkstra mesh', search_dijkstra_mesh)
