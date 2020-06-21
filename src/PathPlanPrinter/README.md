# PathPlanPrinter

Just a simple tool to print planned paths onto a map represented as an image.

## Python version
This code has been tested on Python 3.7. Whilst compatibility with other versions of Python might be possible, it is by no means assured.
Any issues arising as a result of using the wrong version of Python are, therefore, the user's own responsibility.

## Dependencies
* PIL or Pillow
* Numpy

## Download
PathPlanPrinter is hosted in GitHub, so you can clone the repository as usual in Git:
```
git clone https://github.com/R012/PathPlanPrinter.git
```
As an alternative, you can download a zip file with the printer as a direct download (checkout out the green button in the [PathPlanPrinter repository](https://github.com/R012/PathPlanPrinter)).

## Usage
1. Insert the Python source file defining you algorithm into `/src/`. Please, be aware that your algorithm **must** use the definition of a node included in the file `/src/node.py`. For further details, please, refer to said source file and peruse the documentation included within.
2. Register your algorithm into the system. Import `path_planning` into your algorithm's source file, and run the function `register_search_method` included in it. Please, keep in mind that you must indicate the module it is coming from. Therefore, if you do not use an alias for `path_planning`, you will need to call the function using `path_planning.register_search_method`.
   1. This function has no return value, and will throw verbose exceptions if any problems arise.
   2. This function expects two arguments:
      1. A string, identifying the algorithm. This string will be used later on, so making it easily identified is advised.
      2. The function implementing the algorithm. You should not provide a full function call, only its identifier. Thus, if, for example, your function is defined as `a_star(start, goal, grid, heur='naive')`, you would need to pass `a_star` as the second argument for `register_search_method`.
         1. Note that, for the sake of enabling this registering function, it is mandatory that all algorithms take in a starting point, a goal and a heuristic identifier as parameters.
         2. Additionally, take into account that providing anything but a function as an argument will result in faulty behavior. The program will most certainly fail to execute properly, and result in an exception being thrown.
3. Import your algorithm source file at the end of `path_planning.py`, below `aStar` and `dijkstra`. This step is necessary for your algorithm to be loaded into the system.
4. Run `run_path_planning.py` using Python from the command line. Please, keep in mind that you must provide several named arguments for the program to run. Although they are listed in the present file, you may provide the `-h` or `--help` modifier to the python module in order to be presented with further information.
   1. `--scenario`: Path to an image file. This image represents the map over which path planning will be executed. It can use any variation of colors, but bear in mind that black areas will be considered entirely inaccessible, and that darker colors will be considered harder to traverse than lighter ones.
   2. `--algorithm`: String identifying the algorithm you wish to use. This string must have been defined using `path_planning.register_search_method`, along with the corresponding function to call. Failing to comply with either of these conditions will result in an exception being launched.
   3. `--heuristic`: String identifying the heuristic to be used while calculating the shortest path. Please, refer to `/src/heuristics.py` and the subsection `Registering new heuristics` found within this document for more information.
   4. `--start`: Coordinates of the starting point for the path. Must be expressed as a tuple in `"(x, y)"` format. Quotation marks are mandatory in order to ensure proper input. This point existing within the presented scenario is the user's responsibility. Providing an invalid point as argument will result in an exception being thrown.
   5. `--finish`: Coordinates of the goal point for the path. Must be expressed as a tuple in `"(x, y)"` format. Quotation marks are mandatory in order to ensure proper input. This point existing within the presented scenario is the user's responsibility. Providing an invalid point as argument will result in an exception being thrown. Additionally, the program may throw an exception if the goal cannot be reached from the previously defined starting point.
   6. `--grid_size`: Mandatory only if using a grid. Do not use it alongside `--navmesh`. It must be an integer defining the number of divisions to create in both axes over the map. Therefore, a value of, for example, 40, will result in the map being split into a 40x40 grid.
   7. `--navmesh`: Mandatory only if using navigation meshes. Do not use it alongside `--grid_size`. It must be a path to a JSON file defining a navigation mesh for the map. Positions must be expressed in pixels. Ensuring proper definition of the navigation mesh is the user's own responsibility.
5. The resulting path will be stored under the `/out/` folder, as an image displaying the path over the provided map.

### Registering new heuristics

1. Define a function for the new heuristic within `/src/heuristics.py`. Please, note that all heuristic must observe the following conditions:
   1. They must take in two nodes as arguments. You may name them whatever you wish, as long as you keep in mind the underlying data structure.
      For further information about nodes, refer to the file `/src/node.py`.
   2. They must return a numeric value expressing the cost of moving from the first argument to the second.
2. Register the function using a call to `pp.register_heuristic` under the definition of the new heuristic. You must provide a string identifier, as well as the name of the function you are registering, as arguments.

Once both steps are completed, the heuristic will be registered for use automatically within the program. For examples on how to perform this operation, please, refer to `/src/heuristics.py`.

