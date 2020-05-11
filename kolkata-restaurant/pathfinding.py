import queue

def heuristic(a, b):
    x1,y1=a
    x2,y2=b
    return abs(x1 - x2) + abs(y1 - y2)


def Astar(start,goal, walls):
    if start==goal :
        return []
    frontier = queue.PriorityQueue()
    frontier.put((0, start ))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        priority,current=(frontier.get())

        if current == goal:
            break
       
        for next in neighbors(current,walls):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put((priority,next))
                came_from[next] = current
    current = goal 
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def neighbors(current,walls):
    row,col=current
    l=[]
    for t in [(0,1),(0,-1),(1,0),(-1,0)]:
        next_row = row+t[0]
        next_col = col+t[1]
        if (((next_row,next_col) not in walls) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19):
            l.append((next_row,next_col))
    return l
