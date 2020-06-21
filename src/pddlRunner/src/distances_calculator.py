
import os
import sys
sys.path.append(os.path.abspath('./PathPlanPrinter/src'))

import math
from run_path_planning import run_path_planning

class distances_calculator:

  def __init__(self, image, grid_size, algorithm, heuristic, scale,safety_distance=2):
    self.image=image
    self.algorithm=algorithm
    self.heuristic=heuristic
    self.scale=scale
    self.max_distance=None
    self.safety_distance=safety_distance
    self.distances={}
    self.connections=set()
    self.extra_points=[]
    self.grid_size=grid_size
    self.previous_node=()

  def set_max_distance(self, max_distance):
    self.max_distance=max_distance

  def resize(self, point):
    proportions=((self.map_size[0]/self.grid_size[0]),(self.map_size[1]/self.grid_size[1]))
    return (int((point[0]-proportions[0]/2)/proportions[0]), int((point[1]+proportions[1]/2)/(proportions[1])))

  def add_node(self, end):
    r_start=self.resize(self.previous_node)
    r_end=self.resize(end)
    distance=int(math.sqrt(math.pow(self.previous_node[0]-end[0],2)+math.pow(self.previous_node[1]-end[1],2)))
    self.extra_points.append(r_end)
    self.extra_points.append(r_start)
    self.connections.add((r_start,r_end))
    self.connections.add((r_end,r_start))
    self.distances[(r_start,r_end)]=distance
    self.distances[(r_end,r_start)]=distance
    self.previous_node=end

  def make_distance (self, start, end, out=None):
    path = self.run(start, end, out)
    distance = 0
    current_node = path[0]
    extra_points = []
    i=1
    self.previous_node=path[0]
    while i < len(path):
      current_distance=math.sqrt(math.pow(current_node[0]-path[i][0],2)+math.pow(current_node[1]-path[i][1],2))
      if self.max_distance:
        left_to_travel=(len(extra_points)+1)*(self.max_distance-self.safety_distance)
        if (distance+current_distance)>left_to_travel:
          safe_to_go=math.ceil(left_to_travel-distance)
          safe_proportion=current_distance/safe_to_go
          extra_point=(current_node[0]+math.floor((path[i][0]-current_node[0])/safe_proportion),current_node[1]+math.floor((path[i][1]-current_node[1])/safe_proportion))
          self.add_node(extra_point)
          extra_points.append(extra_point)
          distance+=safe_to_go
          current_node=extra_point
        else:
          distance+=current_distance
          current_node=path[i]
          i+=1
      else:
        distance+=current_distance
        current_node=path[i]
        i+=1
    self.add_node(path[len(path)-1])

  def calculate_distances (self, task_points, init_points):
    self.distances={}
    self.extra_points=[]
    self.connections=set()
    for task in task_points:
      for init in init_points:
        self.make_distance(init,task)
    for task1 in task_points:
      for task2 in task_points:
        if task1 != task2:
          self.make_distance(task1,task2)

  def run (self, start, end, out=None):
    path, self.map_size = run_path_planning(f'./PathPlanPrinter/res/{self.image}', None, self.grid_size, self.algorithm, self.heuristic, self.scale, start, end, out)
    return path
    