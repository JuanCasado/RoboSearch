""" This module defines a node from a data-structures POV.

It simply provides the class definition, and serves no purpose on its own.

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


import numpy as np

'''
    Standalone definition of the Node class.
'''
class Node:
    '''
        Class representing a node in an arbitrary navigation mesh.
        It accounts for the possibility of the mesh having been
        constructed by mapping spots in a map to a grid.
    '''
    def __init__(self,value,point, grid_point):
        '''
            Constructor for the Node class.
            Points are represented as a tuple in (x, y) form. Therefore,
            the x component may be accessed via point[0], and the y
            component may be accessed via point[1].
            Likewise, due to the need to map the actual coordinates in
            pixels to a grid in a smaller side, the node stores its
            location in both representation systems. This is necessary
            in order to display it on screen, but either may be used
            for heuristic purposes.
            Inputs:
                - value: numeric value of the spot where the node is
                actually located.
                - point: actual coordinates, in pixels, where the node
                is located.
                - grid_point: mapped coordinates in the grid where the
                node is located. Same as point if there is no grid.
            Output:
                - a Node instance.
        '''
        self.value = int(9 - value/255 * 8)
        self.point = tuple(point)
        self.grid_point = tuple(grid_point)
        self.parent = None
        self.H = 0
        self.G = 0
        self.neighbors = {}
        
    def move_cost(self,other):
        '''
            Calculates the cost to move from this node to another arbitrary node.
            It depends on the distance between them, and the value of the current
            node.
            Inputs:
                - other: node for which the cost of moving needs to be calculated.
            Outputs:
                - numeric value representing the cost of moving from this node to
                the other.
        '''
        v = 0 if self.value == 1 else self.value/9
        dist = np.linalg.norm((self.grid_point[0] - other.grid_point[0],\
                               self.grid_point[1] - other.grid_point[1]))
        return  dist + v

    def register_neighbor(self, neighbor):
        '''
            Registers a new neighbor to this node's list of neighbors.
            Inputs:
                - neighbor: node to be registered as neighbor.
        '''
        self.neighbors[neighbor.point] = neighbor

    def __repr__(self):
        return str(self.point)
