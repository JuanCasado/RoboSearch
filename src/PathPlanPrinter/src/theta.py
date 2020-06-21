
import path_planning as pp

def children(point,grid):
    """
        Calculates the children of a given node over a grid.
        Inputs:
            - point: node for which to calculate children.
            - grid: grid over which to calculate children.
        Outputs:
            - list of children for the given node.
    """
    x,y = point.grid_point
    if x > 0 and x < len(grid) - 1:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y),\
                      (x-1, y-1), (x-1, y+1), (x+1, y-1),\
                      (x+1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x+1,y),\
                      (x-1, y-1), (x+1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y + 1),(x+1,y),\
                      (x-1, y+1), (x+1, y+1)]]
    elif x > 0:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x,y + 1),\
                      (x-1, y-1), (x-1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y),(x,y - 1),(x-1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x-1, y), (x,y + 1), (x-1, y+1)]]
    else:
        if y > 0 and y < len(grid[0]) - 1:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y),(x,y - 1),(x,y + 1),\
                      (x+1, y-1), (x+1, y+1)]]
        elif y > 0:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y),(x,y - 1),(x+1, y-1)]]
        else:
            links = [grid[d[0]][d[1]] for d in\
                     [(x+1, y), (x,y + 1), (x+1, y+1)]]
    return [link for link in links if link.value != 9]

def theta(start, goal, grid, heur='naive', scale=1):
  opened = set()
  closed = set()
  current = start
  opened.add(current)
  while opened:
    current = min(opened, key=lambda node: node.G + node.H)
    pp.expanded_nodes += 1
    if current == goal:
      path = [current]
      while current.parent:
        current = current.parent
        path.append(current)
      return path[::-1]
    opened.remove(current)
    closed.add(current)
    for node in children(current,grid):
      if node in closed: continue
      if current.parent and line_of_sight (current.parent, node):
        new_g = current.parent.G + current.parent.move_cost(node)
        if node in opened:
          if node.G > new_g:
            node.G = new_g
            node.parent = current.parent
        else:
          node.G = new_g
          node.H = pp.heuristic[heur](node, goal, scale)
          node.parent = current.parent
          opened.add(node)
      else:
        new_g = current.G + current.move_cost(node)
        if node in opened:
          if node.G > new_g:
            node.G = new_g
            node.parent = current
        else:
          node.G = new_g
          node.H = pp.heuristic[heur](node, goal, scale)
          node.parent = current
          opened.add(node)
  raise ValueError('No Path Found')
pp.register_search_method('theta', theta)

def is_obstacle(x, y):
  return pp.npdata[int(x)][int(y)]==0

def line_of_sight (n0, n1):
  x0, y0 = n0.point
  x1, y1 = n1.point
  dx = x1 - x0
  dy = y1 - y0
  f = 0
  if dy < 0:
    dy = -dy
    sy = -1
  else:
    sy = 1
  if dx < 0:
    dx = -dx
    sx = -1
  else:
    sx = 1
  if dx >= dy:
    while x0 != x1:
      f += dy
      gx = x0 + (sx - 1)/2
      gy = y0 + (sy - 1)/2
      if f >= dx:
        if is_obstacle(gx, gy):
          return False
        y0 += sy
        f -= dx
      if f!=0 and is_obstacle(gx, gy):
        return False
      if dy==0 and is_obstacle(gx, y0) and is_obstacle(gx, y0-1):
        return False
      x0 += sx
  else:
    while y0 != y1:
      f += dx
      gx = x0 + (sx - 1)/2
      gy = y0 + (sy - 1)/2
      if f >= dy:
        if is_obstacle(gx, gy):
          return False
        x0 += sx
        f -= dy
      if f!=0 and is_obstacle(gx, gy):
        return False
      if dy==0 and is_obstacle(x0, gy) and is_obstacle(x0-1, gy):
        return False
      y0 += sy
  return True



