import json
import path_planning as pp

def clean_tuple(string_tuple):
    clean_list = string_tuple.replace('(', '').replace(')', '').replace(' ', '').split(',')
    return (int(clean_list[0]), int(clean_list[1]))

def run_path_planning(scenario_file, navmesh_file, grid_size, algorithm, heuristic, scale, start, finish, out):
    if type(start) == str:
        start = clean_tuple(start)
    if type(finish) == str:
        finish = clean_tuple(finish)
    if type(scale) != float:
        scale = float(scale)
    pp.load_image(scenario_file)
    print("--------------------------------------------")
    print(f"Running path plan from {start} to {finish}")
    if navmesh_file:
        with open(navmesh_file) as navmesh:
            path = pp.run_path_planning_mesh(navmesh['mesh'],algo=algorithm, heur=heuristic, scale=scale,start=start, finish=finish)
    else:
        if not grid_size:
            print("Please, define a grid size.")
            exit()
        path = pp.run_path_planning(grid_size, algo=algorithm,heur=heuristic, scale=scale, start=start, finish=finish)
    if out:
        pp.output_image(scenario_file, path, out)
    return path, pp.npdata.shape


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(\
        description='Run path planning using a specified scenario.')
    parser.add_argument('--scenario', metavar='s',\
        help='Path to the image file in which the scenario is defined.', required=True)
    parser.add_argument('--out', metavar='o',\
        help='Path to the file where the path will be saved.')
    parser.add_argument('--algorithm', metavar='a',\
                        help='String identifier for the algorithm to '\
                        'use. Caps sensitive.', required=True)
    parser.add_argument('--heuristic', metavar='h',\
                        help='String identifier for the heuristic to '\
                        'use. Caps sensitive.', required=True)
    parser.add_argument('--scale',\
                        help='Sacale factor for the heuristic'\
                        '(heuristic *= scale)')
    parser.add_argument('--start', metavar='s',\
                        help='Tuple defining the starting point in the '\
                        'scenario.', required=True)
    parser.add_argument('--finish', metavar='f',\
                        help='Tuple defining the finishing point in the '\
                        'scenario.', required=True)
    parser.add_argument('--navmesh', metavar='n',\
                        help='Sets the driver to navmesh mode. '\
                        'Path to the JSON file defining '\
                        'the corresponding navmesh. Use only if not '\
                        'running the algorithm over a grid.')
    parser.add_argument('--grid_size', metavar='g',\
                        help='Integer identifying the number of divisions '\
                        'over the X and Y axis of the scenario. Use only if '\
                        'not using navmesh.')
    parser.add_argument('--version', action='store_true', \
            help='Displays the current version of the simulator')
    args = parser.parse_args()
    if args.version:
        print('v.0.0.1')
        exit()
    if not args.scenario:
        print("No scenario file was defined. Please, provide a scenario file.")
        exit()
    if not args.algorithm:
        print("No algorithm was defined.")
        exit()
    if not args.heuristic:
        print("No heuristic was defined.")
        exit()
    if not args.start:
        print("No starting point was defined.")
        exit()
    if not args.finish:
        print("No finishing point was defined.")
        exit()
    if not args.finish:
        print("No finishing point was defined.")
        exit()
    if not args.scale:
        scale = 1
    else:
        scale = args.scale
    run_path_planning(args.scenario, args.navmesh, clean_tuple(args.grid_size),
                    args.algorithm, args.heuristic, scale,
                    clean_tuple(args.start), clean_tuple(args.finish),
                    args.out)
