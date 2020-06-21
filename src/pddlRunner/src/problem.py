
from functools import reduce
from utils import group

class problem:

  def __init__(self, description, distance_calculator):
    self.description = description
    self.task_points = tuple(set([tuple(task["point"]) for task in self.description["goals"]]))
    self.init_points = tuple(set([tuple(robot["init"]) for robot in self.description["robots"]]))
    self.tasks = set([task["action"] for task in self.description["goals"]])
    distance_calculator.set_max_distance(self.get_min_distance())
    distance_calculator.calculate_distances(self.task_points, self.init_points)
    self.distances=distance_calculator.distances
    self.connections=distance_calculator.connections
    points=[]
    points.extend(self.task_points)
    points.extend(self.init_points)
    points.extend(distance_calculator.extra_points)
    self.points = list(set(points))
    print(self.connections)

  def get_min_distance(self):
    distance=float('inf')
    for robot in self.description['robots']:
      for speed in robot['speeds']:
        current_distance=(robot['maxBattery']/speed['consume'])*speed['speed']
        if current_distance < distance:
          distance=current_distance
    return distance
    
  def get_robots(self):
    return reduce(group, [robot["name"] for robot in self.description["robots"]])

  def get_locations(self):
    return reduce(group, [f"LOCATION{point_index}" for point_index, _ in enumerate(self.points)])

  def get_speeds(self):    
    speeds = set()
    for robot in self.description["robots"]:
      for speed in robot["speeds"]:
        speeds.add(speed["name"])
    return reduce(group, speeds)

  def get_tasks(self):
    return reduce(group, self.tasks)

  def describe_robots(self):
    def describe_robot(robot):
      robot_name=robot["name"]
      def describe_speed(speed):
        name=speed["name"]
        consume=speed["consume"]
        value=speed["speed"]
        return (
          f"(= (speed {robot_name} {name}) {value})"
          f"(= (moveBurn {robot_name} {name}) {consume})\n"
      )
      def describe_tasks(task):
        name=task["name"]
        if name not in self.tasks:
          return ""
        consume=task["consume"]
        duration=task["duration"]
        return (
          f"(= (taskDuration {robot_name} {name}) {duration}) (= (taskBurn {robot_name} {name}) {consume})\n"
        )
      init=self.points.index(tuple(robot["init"]))
      speeds=robot["speeds"]
      tasks=robot["tasks"]
      battery=robot["battery"]
      maxBattery=robot["maxBattery"]
      rechargeRate=robot["rechargeRate"]
      return (
        f"(at {robot_name} LOCATION{init})\n"
        f"{reduce(group, [describe_speed(speed) for speed in speeds])}"
        f"(= (battery {robot_name}) {battery}) (= (maxBattery {robot_name}) {maxBattery}) (= (rechargeRate {robot_name}) {rechargeRate})\n"
        f"{reduce(group, [describe_tasks(task) for task in tasks])}\n"
      )
    return reduce(group, [describe_robot(robot) for robot in self.description["robots"]])

  def init_tasks (self):
    acc=""
    for task in self.tasks:
      for point,_ in enumerate(self.points):
        acc+=f"(= (tasks LOCATION{point} {task}) 0)"
    return acc

  def get_goal (self):
    def describe_goal(goal):
      point=goal["point"]
      action=goal["action"]
      times=goal["times"]
      return (
        f"(= (tasks LOCATION{self.points.index(tuple(point))} {action}) {times})\n"
      )
    return reduce(group, [describe_goal(goal) for goal in self.description["goals"]])

  def describe_distances(self):
    def describe_distance(distance):
      start=self.points.index(distance[0])
      end=self.points.index(distance[1])
      if distance in self.connections:
        dist=self.distances[distance]
        return f"(= (distance LOCATION{start} LOCATION{end}) {dist})"
      else:
        return ""
        dist=999
        return f"(= (distance LOCATION{start} LOCATION{end}) {dist})"
    points_join=[]
    for point1 in self.points:
      for point2 in self.points:
        points_join.append((point1, point2))
    return reduce(group, [describe_distance(distance) for distance in points_join])

  def describe_connections(self):
    def describe_connection(connection):
      start=self.points.index(connection[0])
      end=self.points.index(connection[1])
      return f"(connected LOCATION{start} LOCATION{end})"
    return reduce(group, [describe_connection(connection) for connection in self.connections])

  def describe_metric(self):
    metrics=['totalTime','totalBattery','totalDistance','recharges']
    if self.description['metric'] in metrics:
      return f"(:metric minimize ({self.description['metric']}))"
    else:
      return ""

  def __repr__(self):
    return self.__str__

  def __str__(self):
    return (
      f"(define (problem probPlanetary) (:domain planetary) (:objects\n"
      f" {self.get_robots()} - robot\n"
      f" {self.get_locations()} - location\n"
      f" {self.get_speeds()} - speedType\n"
      f" {self.get_tasks()} - taskType\n"
      f")\n(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)\n"
      f" {self.describe_robots()}\n"
      f" {self.init_tasks()}\n\n"
      f" {self.describe_distances()}\n\n"
      f" {self.describe_connections()}\n\n"
      f")(:goal (and\n"
      f" {self.get_goal()}"
      f"))\n"
      f" {self.describe_metric()}\n"
      f")\n"
    )

