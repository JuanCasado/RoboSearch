
import re

head_path='./pddlRunner/problems/'

def generate_task_list(task_list):
  tasks = []
  for line in task_list:
    if re.match(r'^\(\w(\w|_)*(\ *(\w(\w|_)*)?)*\)', re.sub(r"(\d(\.|\d)*: ) *", "", line)):
      split_line = re.sub(r"(\d(\.|\d)*: ) *", "", line).split()
      tasks.append(split_line[0].replace('(', '').replace(')', ''))
      time_stamp=line.split(':',1)[0]
      if tasks[-1].lower() == 'move':
        coord1 = split_line[2].replace('location', '').replace(')', '')
        coord2 = split_line[3].replace('location', '').replace(')', '')
        tasks[-1] = (tasks[-1], split_line[1], int(coord1), int(coord2), split_line[4].replace(')', ''), float(split_line[5].replace('[', '').replace(']', '')))
        tasks[-1] = {'task': tasks[-1][0], 'who': tasks[-1][1], 'from': tasks[-1][2], 'to': tasks[-1][3], 'with': tasks[-1][4], 'in': tasks[-1][5], 'time':time_stamp}
      elif tasks[-1].lower() == 'recharge':
        tasks[-1] = (tasks[-1], split_line[1], int(split_line[2].replace('location', '').replace(')', '')), float(split_line[3].replace('[', '').replace(']', '')))
        tasks[-1] = {'task': tasks[-1][0], 'who': tasks[-1][1], 'at': tasks[-1][2], 'in': tasks[-1][3], 'time':time_stamp}
      elif tasks[-1].lower() == 'performtask':
        coord = split_line[2].replace('location', '').replace(')', '')
        tasks[-1] = (tasks[-1], split_line[1], int(coord), split_line[3].replace(')', ''), float(split_line[4].replace('[', '').replace(']', '')))
        tasks[-1] = {'task': tasks[-1][0], 'who': tasks[-1][1], 'at': tasks[-1][2], 'what': tasks[-1][3], 'in': tasks[-1][4], 'time':time_stamp}
  return tasks

def parse_execution(problem_name, execution, path_planner, points):
  tasks=generate_task_list(execution)
  html=''
  html_to_save=''
  for index, task in enumerate(tasks):
    if task['task']=='recharge':
      new_content=f'<p>[{task["time"]}] {task["who"]} recharged at {points[task["at"]]} in {task["in"]}</p>\n'
      html+=new_content
      html_to_save+=new_content
    elif task['task']=='performtask':
      new_content=f'<p>[{task["time"]}] {task["who"]} {task["what"]} at {points[task["at"]]} in {task["in"]}</p>\n'
      html+=new_content
      html_to_save+=new_content
    elif task['task']=='move':
      new_content=f'<p>[{task["time"]}] {task["who"]} moved from {points[task["from"]]} to {points[task["to"]]} in {task["in"]}</p>\n'
      html+=new_content
      html_to_save+=new_content
      path_planner.run(points[task['from']], points[task['to']], f'./pddlRunner/problems/{problem_name}/action_{index}.png')
      html+=f"<img src='/image/{problem_name}/action_{index}.png'/>\n"
      html_to_save+=f"<img src='action_{index}.png'/>\n"
  with open(f'./pddlRunner/problems/{problem_name}/out.html', 'w+') as html_file:
    html_file.write(f'<!DOCTYPE html><html><head></head><body>\n{html_to_save}</body></html>')
  return html
  