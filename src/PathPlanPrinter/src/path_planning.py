""" This module defines general path planning utilities.

It accounts for two different kinds environments over which to perform
path planning: grid-based, and navigation mesh-based.

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
import math
import time
from PIL import Image

import PathPlanPrinter as printer

from node import Node

search_methods = {}
heuristic = {}

expanded_nodes = 0

npdata = None
grid_size = []

def register_search_method(label, function):
    """
        Registers a new search method to be selected and used on runtime
        if necessary.
        Inputs:
            - label: string representing the function. Can have any sort
            of format, provided that the host admits it.
            - function: function pointer to the function implementing the
            search method in question.
    """
    global search_methods
    def function_caller (label, function, args):
        start = time.time()
        print(f'Search algorithm {label} with heuristic {args[3]} * {args[4]}')
        try:
            return function(args[0],args[1],args[2], args[3], args[4])
        finally:
            now = time.time()
            print(f'Search algorithm took: {now - start}s')


    search_methods[label] = lambda *args : function_caller(label, function, args)

def register_heuristic(label, function):
    """
        Registers a new heuristic to be selected and used on runtime if
        necessary.
        Inputs:
            - label: string representing the heuristic. Can have any sort
            of format, provided that the host admits it.
            - function: function pointer to the function implementing the
            heuristic in question.
    """
    global heuristic
    heuristic[label] = function

def generate_grid(npdata, divider):
    """
        Auxiliary function that creates a grid using map data as a reference.
        Inputs:
            - npdata: map data represented as an nparray.
            - divider: number of divisions to perform per axis.
        Outputs:
            - grid of numbers representing the values of each tile of the
            generated grid.
            - width of each tile of the grid.
            - height of each tile of the grid.
    """
    map_size = npdata.shape
    npdata = npdata.copy()
    if type(divider) is list or type(divider) is tuple:
        chunk_width = map_size[0]/divider[0]
        chunk_height = map_size[1]/divider[1]
    else:
        chunk_width = map_size[0]/divider
        chunk_height = map_size[1]/divider
        divider = [divider, divider]
    print(f'Map Size: {map_size}')
    print(f'Chunk Size: ({chunk_width}, {chunk_height})')
    grid = []
    for i in range(divider[1]):
        row = []
        for j in range(divider[0]):
            value = npdata.item(int(j*chunk_width+chunk_width/2), int(i*chunk_height+chunk_height/2))
            for k in range(int(chunk_height)):
                for l in range(int(chunk_width)):
                    if npdata.item(int(j*chunk_width + l), int(i*chunk_height+k)) is 0:
                        value=0
                        break
            row.append(value)
            for y in range(int(i*chunk_height), int(i*chunk_height+chunk_height)):
                for x in range(int(j*chunk_width), int(j*chunk_width+chunk_width)):
                    npdata[x, y] = row[j]
        grid.append(row)
    return grid, chunk_width, chunk_height

def generate_grid_no_divider(npdata):
    """
        Auxiliary function that creates a grid using map data as a reference.
        Inputs:
            - npdata: map data represented as an nparray.
            - divider: number of divisions to perform per axis.
        Outputs:
            - grid of numbers representing the values of each tile of the
            generated grid.
            - width of each tile of the grid.
            - height of each tile of the grid.
    """
    map_size = npdata.shape
    npdata = npdata.copy()
    chunk_width = 1
    chunk_height = 1
    grid = []
    for i in range(map_size[1]):
        row = []
        for j in range(map_size[0]):
            value = npdata.item(j, i)
            row.append(value)
        grid.append(row)
    return grid, chunk_width, chunk_height

def create_grid(npdata, divider):
    """
        Auxiliary function that generates a grid of nodes. Generally, use this rather than generate_grid.
        Inputs:
            - npdata: map data represented as an nparray.
            - divider: number of divisions to perform per axis.
        Outputs:
            - fully configured grid of nodes.
    """
    grid, w, h = generate_grid(npdata, divider)
    g = []
    for j in range(len(grid[0])):
        row = []
        for i in range(len(grid)):
            val = grid[i][j]
            n = Node(grid[i][j], (int(j*w+w/2),int(i*h+h/2)), (j, i))
            row.append(n)
        g.append(row)
    grid = g
    return grid

def create_grid_no_divider(npdata):
    """
        Auxiliary function that generates a grid of nodes. Generally, use this rather than generate_grid.
        Inputs:
            - npdata: map data represented as an nparray.
            - divider: number of divisions to perform per axis.
        Outputs:
            - fully configured grid of nodes.
    """
    grid, w, h = generate_grid_no_divider(npdata)
    g = []
    for j in range(len(grid[0])):
        row = []
        for i in range(len(grid)):
            val = grid[i][j]
            n = Node(grid[i][j], (int(j*w+w/2),int(i*h+h/2)), (j, i))
            row.append(n)
        g.append(row)
    grid = g
    return grid

def generate_neighbors(node, nodes):
    """
        Auxiliary function that calculate the neighbors of a given node within a navigation mesh.
        Inputs:
            - node: node for which to calculate the neighbors.
            - nodes: list of all the nodes conforming the mesh.
    """
    found = {}
    for n in nodes.values():
        if n is node:
            continue # We want to ignore the node for which we are currently generating neighbors
        # Calculate the angle of the vector between nodes
        angle = math.degrees(math.atan2(n.point[1] - node.point[1], n.point[0] - node.point[0]))
        if angle in found:  # There was already a node in that angle
            if u.los_raycasting(node.point, n.point, u.npdata) == (-1, -1): # There is line of sight
                new_dist = np.linalg.norm((node.point[0] - n.point[0], node.point[1] - n.point[1]))
                cur_dist = np.linalg.norm((node.point[0] - found[angle].point[0], node.point[1] - found[angle].point[1]))
                if new_dist < cur_dist: # We have found a better alternative than what we already had
                    found[angle] = n
        else:
            if u.los_raycasting(node.point, n.point, u.npdata) is None: # There is line of sight
                found[angle] = n # There was nothing stored, so we just save the current node in that direction
    node.neighbors = found # Replace the list of neighbors so they can be explored later
        

def generate_navmesh(npdata, waypoints):
    """
        Function that creates a navigation mesh, given a map and a list of waypoints.
        Inputs:
            - npdata: map data, represented as an nparray.
            - waypoints: list of waypoints that conform the nav mesh.
        Outputs:
            - a fully configured nav mesh, represented as a dictionary of nodes.
    """
    nodes = {}
    for w in waypoints:
        nodes[tuple(w)] = Node(npdata.item(int(w[0]), int(w[1])), w, w)
    for n in nodes.values():
        generate_neighbors(n, nodes)
    return nodes

def generate_waypoints_list(algo, start, finish, grid, heur="naive", scale=1):
    """
        Generates an ordered list of waypoints for a controller to iterate over.
        Inputs:
            - algo: string representing the path planning algorithm to be used.
            - start: node from which to start, represented as a tuple of coordinates.
            - finish: goal node, represented as a tuple of coordinates.
            - grid: grid over which to plan the path.
            - heur: heuristic to be used, in case the algorithm requires it, represented
            as a string.
        Outputs:
            - ordered list of waypoints conforming the planned path.
    """
    global search_methods, expanded_nodes
    nodes = search_methods[algo](grid[start[0]][start[1]], grid[finish[0]][finish[1]], grid, heur, scale)
    waypoints = []
    cost = 0
    for n in nodes:
        cost += n.value
        waypoints.append(n.point)
    printer.print_waypoints(waypoints, cost, expanded_nodes)
    return waypoints

def generate_waypoints_list_mesh(algo, start, finish, mesh, heur="naive", scale=1):
    """
        Generates an ordered list of waypoints for a controller to iterate over.
        Inputs:
            - algo: string representing the path planning algorithm to be used.
            - start: node from which to start, represented as a tuple of coordinates.
            - finish: goal node, represented as a tuple of coordinates.
            - mesh: navigation mesh over which to plan the path.
            - heur: heuristic to be used, in case the algorithm requires it, represented
            as a string.
        Outputs:
            - ordered list of waypoints conforming the planned path.
    """
    global search_methods, expanded_nodes
    nodes = search_methods[algo](mesh[tuple(start)], mesh[tuple(finish)], mesh, heur, scale)
    waypoints = []
    cost = 0
    for n in nodes:
        waypoints.append(n.point)
        cost += n.value
    printer.print_waypoints(waypoints, cost, expanded_nodes)
    return waypoints

def run_path_planning(grid_sze, algo='A*', start=(1, 1), finish=(2,2), heur='naive', scale=1, show_grid=True):
    """
        Configures and runs a given path planning algorithm over a grid.
        Inputs:
            - grid_size: number of divisions to perform on the simulation's map in both axis.
            - algo: string representing the algorithm to be used.
            - start: coordinates of the node at which to begin planning the path.
            - finish: coordinates of the goal node.
            - heur: heuristic to be used, if necessary, represented as a string.
        Outputs:
            - ordered list of nodes to be visited representing the planned path.
    """
    global npdata, grid_size
    npdata = np.rot90(npdata)
    npdata = np.flipud(npdata)
    grid = create_grid(npdata, grid_sze)
    res = generate_waypoints_list(algo, start, finish, grid, heur, scale)
    npdata = np.flipud(npdata)
    npdata = np.rot90(npdata, k=3)
    div = 10
    if type(grid_sze) is list or type(grid_sze) is tuple:
        width, height = npdata.shape[0]/grid_sze[1], npdata.shape[1]/grid_sze[0]
    else:
        width, height = npdata.shape[0]/grid_sze, npdata.shape[1]/grid_sze
    grid_size = [width, height]
    return res

def run_path_planning_mesh(mesh_points, algo='A* mesh', scale=1, start=(1, 1), finish=(2, 2), heur='naive'):
    """
        Configures and runs a given path planning algorithm over a mesh.
        Inputs:
            - mesh_points: list of waypoints that form the navigation mesh.
            - algo: string representing the algorithm to be used.
            - start: coordinates of the node at which to begin planning the path.
            - finish: coordinates of the goal node.
            - heur: heuristic to be used, if necessary, represented as a string.
        Outputs:
            - ordered list of nodes to be visited representing the planned path.
    """
    global npdata
    npdata = np.rot90(u.npdata)
    npdata = np.flipud(u.npdata)
    mesh = generate_navmesh(u.npdata, mesh_points)
    res = generate_waypoints_list_mesh(algo, start, finish, mesh, heur, scale)
    npdata = np.flipud(u.npdata)
    npdata = np.rot90(u.npdata, k=3)
    return res

def load_image(infilename):
    """
        Helper function that loads an image in black and white, then returns it as an nparray.
    """
    global npdata
    img = Image.open(infilename).convert("L")
    img.load()
    npdata = np.asarray(img, dtype="int32")

def output_image(name, path, out_path=''):
    global grid_size
    if out_path=='':
        pathPrinter = printer.PathPlanPrinter(input_file=name, plan=path, grid_size=grid_size)
    else:
        pathPrinter = printer.PathPlanPrinter(input_file=name, plan=path, grid_size=grid_size, output_file=out_path)
    pathPrinter.draw_plan()
    pathPrinter.print_plan()

import heuristics
import aStar
import dijkstra
import theta