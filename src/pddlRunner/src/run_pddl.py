

import distances_calculator
import execution_parser
import problem
from functools import reduce
from utils import group
import utils
import json
import os, sys, subprocess

head_path='./pddlRunner/problems/'
problem_path='/problem.pddl'
execution_path='/pddl.txt'
domain_path='./pddlRunner/domains/planetary.pddl'

def run_json(str_problem):
  json_problem=json.loads(str_problem)
  problem_name=json_problem['name']
  if not os.path.exists(f'{head_path}{problem_name}'):
    os.makedirs(f'{head_path}{problem_name}')
  with open(f'{head_path}{problem_name}/{problem_name}.json', 'w+') as problem_file:
    problem_file.write(repr(str_problem)[2:-1])
  path_planner, prob=create_problem (json_problem, problem_name)
  execution=run_pddl(problem_name)
  out=execution_parser.parse_execution(problem_name, execution, path_planner, prob.points)
  print(out)
  print('Execution compled!!!')
  return out

def run_pddl (problem_name):
  running_process = subprocess.Popen(f"optic-clp {domain_path} {head_path}{problem_name}{problem_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
  out=[]
  add_to_out=False
  end=False
  skipped=0
  to_skip=3
  while running_process.poll() is None and not end:
    line=running_process.stdout.readline()
    if add_to_out:
      if skipped < to_skip:
        skipped+=1
      elif 'Resorting to best-first search' in line:
        add_to_out=False
        end=True
        running_process.terminate()
        running_process.kill()
      else:
        out.append(line)
    elif 'Plan found with metric' in line:
      add_to_out=True
    print(line, end='')
  if end:
    print('PLAN FOUND!!!')
  else:
    print('PLAN NOt FOUND :(')
  with open(f'{head_path}{problem_name}{execution_path}', 'w+') as execution_output:
    execution_output.write(reduce(group, out))
  return out
      

def create_problem (parsed_problem_description, output):
  path_planner = distances_calculator.distances_calculator(parsed_problem_description['image'], parsed_problem_description['pathPlan']['grid_size'], parsed_problem_description['pathPlan']['algorithm'], parsed_problem_description['pathPlan']['heuristic'], parsed_problem_description['pathPlan']['scale'])
  prob = problem.problem(parsed_problem_description,path_planner)
  if not os.path.exists(f'{head_path}{output}'):
    os.makedirs(f'{head_path}{output}')
  with open(f'{head_path}{output}{problem_path}', 'w+') as problem_output:
    problem_output.write(str(prob))
  return path_planner, prob
  


if __name__ == '__main__':
  with open('./pddlRunner/json/problem_description.json') as problem_description:
    str_problem = problem_description.read()
  run_json(str_problem)
  
  
