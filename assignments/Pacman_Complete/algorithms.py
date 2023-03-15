
def dijkstra(nodes, start_node):
    nodes_dict = nodes.costs
    unvisited_nodes = list(nodes.costs)
    previous_nodes = {node: None for node in unvisited_nodes}
    shortest_path = {node: float('inf') for node in unvisited_nodes}
    shortest_path[start_node] = 0

    while unvisited_nodes:
      current = min(unvisited_nodes, key=shortest_path.get)

      unvisited_nodes.remove(current)  # mark the current node as visited
      
      neighbors = nodes_dict[current]

      for neighbor in neighbors:
        tentative_value = shortest_path[current] + 1 
        if tentative_value < shortest_path[neighbor]:
            shortest_path[neighbor] = tentative_value
            previous_nodes[neighbor] = current


    return shortest_path, previous_nodes

def astar(start, goal, nodes, heuristic):

    nodes_dict = nodes.costs
    unvisited = list(nodes.costs)
    visited = set()

    came_from = {}
    f_scores = {node: float('inf') for node in unvisited}
    g_scores = {node: float('inf') for node in unvisited}

    f_scores[start] = heuristic(start,goal)
    g_scores[start] = 0

    while unvisited:
        current_node = min(unvisited, key=f_scores.get)

        if current_node == goal:
            path = [current_node]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()
            return path

        unvisited.remove(current_node)
        visited.add(current_node)

        neighbors = nodes_dict[current_node]

        for neighbor in neighbors: 
            if neighbor in visited:
                continue

            tentative_g_score = g_scores[current_node] + 1
            if neighbor not in unvisited or tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current_node
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in unvisited:
                    unvisited.add(neighbor)

    return [0]*100 #If we can't find a path, the ghost is locked and possesses no threat

def heuristic(start, goal):
    vec = start.position - goal.position
    return vec.magnitudeSquared()


    #return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

def manhatan_distance(start, goal):
    vec = start.position - goal.position
    return abs(vec.x) + abs(vec.y)