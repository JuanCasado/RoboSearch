
# Robot-Planner

A path and a task planner have been integrated to create a decision system that could be able to command a set of robots to perform a set of tasks.
Combining both planner clear plan instructions can be obtained.

A robot could follow those instructions and use this same planner online for re-planning purposes if the current and the expected state diverge.

Plans can be obtained to command any number of robots to perform any number tasks.
A task can happen at any place multiple times.
The planner also takes care of recharging the robots batteries.

## Run the code

The code included a website to help building the plans, execute them and help their exploration.

Docker is the only requirement for executing this program [Download link](https://www.docker.com/get-started)
download it for your platform and follow installation instructions.

* Map images are expected at [./src/PathPlanPrinter/res](./src/PathPlanPrinter/res)
* Output will be left at [./src/pddlRunner/problems](./src/pddlRunner/problems)
* Web interface is available at [http://localhost:80](http://localhost:80)

```bash
# At root directory (where docker-compose.yml is located)
docker-compose up
```

### Problems at runtime

The most common problems:

* Images do not exist at the expected location.
* Robot or task names are not supported by pddl.

## Path planning

The implemented path planning algorithms are run over a fix grid map.
This is not the best representation for every type of map, it specially struggles with large and monotonic maps.
Dijkstra and A* algorithms also support mesh/graph maps but that support has not been ported to the rest of the code which expect a fixed grid map.
The fixed grid map is created from an image and a grid size.

General path planning algorithms are included:

* **Dijkstra algorithm**: will always find the best path but uses too much resources.
* **A* algorithm**: if the heuristic is admisible will wind the best path.
  Sometimes it is worth tricking the heuristic to be none admisible (multiplying it by a factor).
  This will not provide an optimal path but resources will be saved.
  Then the algorithms will behave as an in between of Dijkstra and greedy search.
* **Theta algorithm**: version of A* that eliminates intermediate nodes according to visibility between them.
  This will create more optimal and realistic paths that do not necessarily follow the grid.

### Heuristics

The heuristic implementation has been taken from [Stanford.edu](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html).

* **Manhattan**: great for maps that allow 4 movements at each grid point.
* **Octile**: great for maps that allow 8 movements at each grid point.
* **Chebyshev**: great for maps that allow 4 movements at each grid point.
* **Euclidean**: great for maps that allow any movement at each grid point.

Every heuristic implemented can be configured with a scale factor.
This cale factor directly multiplies the value obtained from the heuristic.
If it is about the correct magnitude will reduce the amount of nodes that are expanded.

* A scale factor of 0 transforms A* in dijkstra algorithm.
* A scale factor of infinite transforms A* in a greedy algorithm that strictly follows the provided heuristic.
* The ideal scale factor is about: (minimum cost of taking one step)/(expected maximum path length)

To perform estimations the heuristics calculate distances in pixels (NOT IN GRID DISTANCES!!!).

## Task planning

Each robot can have its own set of tasks that it can perform different from the others.

```lisp
(= (taskDuration ROBOT1 DRILL) 40) (= (taskBurn ROBOT1 DRILL) 3)
(= (taskDuration ROBOT1 PHOTO) 30) (= (taskBurn ROBOT1 PHOTO) 1)
(= (taskDuration ROBOT2 DRILL) 10) (= (taskBurn ROBOT2 DRILL) 2)
```

ROBOT1 can DRILL and PHOTO but ROBOT2 can only DRILL.
Each one of them can perform each task with different durations and consumptions.

Each robot also has a battery that can robt be drained.

```lisp
(= (battery ROBOT1) 90) (= (maxBattery ROBOT1) 300) (= (rechargeRate ROBOT1) 0.001)
(= (battery ROBOT2) 20) (= (maxBattery ROBOT2) 400) (= (rechargeRate ROBOT2) 0.005)
```

The batter has a initial capacity, a max capacity and a recharge rate.
Moving, and performing tasks drain the battery according to the burn rate and the time taken to perform the action or movement.
Recharging the battery takes time according to the battery left and the recharge rate.

Each robot can move at its own set of speeds.

```lisp
(= (speed ROBOT1 FAST) 40)(= (moveBurn ROBOT1 FAST) 4)
(= (speed ROBOT1 SLOW) 20)(= (moveBurn ROBOT1 SLOW) 3)
(= (speed ROBOT2 SLOW) 10)(= (moveBurn ROBOT2 SLOW) 1)
```

The speed is expressed in pixels per unit of time.
The distance between points is also measured in pixels.

Goals are provided in a general way.
There is not a specific robot that must do each action, each robot that can perform the specific action is up to do it.
The planner will decide which robot should perform the action.

```lisp
(= (tasks LOCATION4 DRILL) 3)
(= (tasks LOCATION0 PHOTO) 2)
(= (tasks LOCATION0 DRILL) 4)
(= (tasks LOCATION5 DRILL) 2)
(= (tasks LOCATION1 PHOTO) 6)
```

This examples can also be represented as:

```json
{
  "robots":[
    {
      "name":"ROBOT1","battery":90,"maxBattery":300,"rechargeRate":0.001,"init":[30,10],
      "speeds":[
        {"name":"FAST","speed":40,"consume":4},
        {"name":"SLOW","speed":20,"consume":3}
      ],
      "tasks":[
        {"name":"DRILL","duration":40,"consume":4},
        {"name":"PHOTO","duration":30,"consume":3}]
      },
    {
      "name":"ROBOT2","battery":20,"maxBattery":400,"rechargeRate":0.005,"init":[8,20],
      "speeds":[
        {"name":"SLOW","speed":10,"consume":1}
      ],
      "tasks":[
        {"name":"PHOTO","duration":10,"consume":1}
      ]
    }
  ],
  "goals":[
    {"point":[27,19],"action":"DRILL","times":3},
    {"point":[30,30],"action":"PHOTO","times":2},
    {"point":[30,30],"action":"DRILL","times":4},
    {"point":[15,15],"action":"DRILL","times":2},
    {"point":[9,9],"action":"PHOTO","times":6}
  ]
}
```

## Integration

Path planners can decide the optimal route between two points in a map.
Task planners can order timed tasks to minimice the time taken to do them as well as follow the constrain restrictions (preconditions) of each task.

To plan what a mobile robot should do both are needed.

* A path planner cannot do what a task planner can.
* The task planner is way to slow calculating path plans, they are too general.

In this case the integration of the path and the task planner is performed in three steps.

### Calculate relevant points and distances between them

Plans are written in JSON instead of in PDDL.
This JSON representation is used to calculate relevant points.
A point is relevant if:

* A robot starts is it.
* A task needs to happen in it.
* If it did not exist at least one robot could not reach one relevant point from another by following the best path between them because it would have enough battery.
  (robots can only recharge when they are not moving)

To calculate the relevant points and the distances between them path planning is used.

With the relevant points calculated and the other information contained in the JSON file an optimized plan in pddl is generated.
This plan is optimized in the sense that is omits none relevant information.
The dull parts of writing a pddl problem are omitted by generating it from another better data representation.

### Calculate order of the tasks

[Optic](https://nms.kcl.ac.uk/planning/software/optic.html)
task planner is run with the generated problem and the domain in [./src/pddlRunner/domains](./src/pddlRunner/domains)

Also sg-plan can be used but the plan generation can take way more time depending on the complexity of the problem.

We do not wait for the best plan that Optic can provide, the first outputted plan is used and the process is killed.
This produces none optimal solution but good enough ones, and take just a small amount of time.

### Obtain real routes

Finally the plan output is retrieved from optic.
This plan is then parsed and real routes are calculated for the actual movements that the robots should perform.
Also a web page is generated to display the formatted plan output as well as images displaying the robots movements.

## Next steps

Only a path planner and a task planner to solve an specific domain are provided.
This is not enough to control a real robot even if the domain adapts to the robot domains.

State estimation is needed to detect deviations from the expected sate is needed.
This involves reading sensors, and transform those inputs into useful information which mighty involve localization, SLAM, object detection and many other techniques.
Then a replanning policy can be implemented which could reuse this planner.

Additionally other important parts of the robotics field may be needed like obstacle avoidance.
