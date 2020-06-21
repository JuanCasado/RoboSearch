""" This module implements several heuristics.

They assume the Node class provided with this simulator is being used.

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


import path_planning as pp
import math

def naive(point1, point2, scale=1):
    return scale
pp.register_heuristic('naive', naive)


def dijkstra(point1, point2, scale=1):
    return 0 * scale
pp.register_heuristic('dijkstra', dijkstra)


def manhattan(point1, point2, scale=1):
    return scale * (abs(point1.point[0] - point2.point[0]) + abs(point1.point[1] - point2.point[1]))
pp.register_heuristic('manhattan', manhattan)


def euclidean(point1, point2, scale=1):
    return scale * math.sqrt(math.pow(point1.point[0] - point2.point[0], 2) + math.pow(point1.point[1] - point2.point[1], 2))
pp.register_heuristic('euclidean', euclidean)


def diagonal(point1, point2, mode, scale=1):
    d0 = abs(point1.point[0] - point2.point[0])
    d1 = abs(point1.point[1] - point2.point[1])
    return scale * (d0 + d1) + (mode - 2 * scale) * min(d0, d1)


def octile(point1, point2, scale=1):
    return diagonal(point1, point2, math.sqrt(2), scale)
pp.register_heuristic('octile', octile)


def chebyshev(point1, point2, scale=1):
    return diagonal(point1, point2, 1, scale)
pp.register_heuristic('chebyshev', chebyshev)
