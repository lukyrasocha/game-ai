from vector import Vector2
from algorithms import astar, heuristic, manhatan_distance

class Task(object):
    def __init__(self):
        # Holds a list of the children (if any) of this task
        self.children
    
    # Always terminates with either success (True) or failure (False)
    def run(self):
        return 

class Selector(Task):
    def __init__(self, children):
        self.children = children
    
    def run(self):
        for c in self.children:
            if c.run():
                return True
        return False

class Sequence(Task):
    def __init__(self, children):
        self.children = children 
    
    def run(self):
        for c in self.children:
            if not c.run():
                return False
        return True

class GhostsNearby(Task):
    def __init__(self, threshold, pacman_node, ghosts, nodes):
        self.threshold = threshold
        self.nodes = nodes #Graph
        self.pacman_node = pacman_node
        self.ghosts = ghosts

    def run(self):
      distances = []
      for ghost in self.ghosts:
        path = astar(self.pacman_node, ghost.target, self.nodes, heuristic)

        if path is None:
          # If no path is found, assume a very large distance
          distances.append(1000000) 
        else:
          distances.append(len(path))
      
      # Check if any of the distances are less than or equal to the threshold
      print("=====FIRST STEP OF SEQUENCER ======")
      if any(distance <= self.threshold for distance in distances):
          print(distances)
          print("TRUE")
          return True 
      else:
          print("FALSE")
          return False 

class FleeFromGhosts(Task):
    def __init__(self, nodes, pacman, ghosts):
      self.nodes = nodes
      self.ghosts = ghosts
      self.pacman = pacman
      
    def run(self):
      list_of_nodes = list(self.nodes.costs)
      candidate_locations = set()

      for node in list_of_nodes:
        if all(len(astar(node, ghost.target, self.nodes, heuristic)) > 5 for ghost in self.ghosts):
               #all(manhatan_distance(node, ghost) > 5 for ghost in self.ghosts):
            candidate_locations.add(node)

      # Find the shortest path from Pac-Man to each candidate safe location 
      safe_distances = {}
      safe_paths = {}
      for location in candidate_locations:
          path = astar(self.pacman.node, location, self.nodes, heuristic)
          if path is not None:
              safe_distances[location] = len(path)
              safe_paths[location] = path


      if not safe_distances:
        return False 

      print("====== SECOND STEP OF THE SEQUENCER ========")
      #for node in safe_distances:
          #print(node, safe_distances[node])

      chosen_location = min(safe_distances, key=safe_distances.get)
      print("CHOSEN", chosen_location, safe_distances[chosen_location])
      self.pacman.directionMethod = self.pacman.goalDirection
      #self.pacman.target = safe_paths[chosen_location][0]
      self.pacman.goal = chosen_location.position

      return True



class EnemyFar(Task):
    def __init__(self, distanceToEnemy):
        self.distanceToEnemy = distanceToEnemy

    def run(self):
        if self.distanceToEnemy[0] >= 15 or self.distanceToEnemy[1] >= 15:
            return True
        else:
            return False

class EnemyNear(Task):
    def __init__(self, distanceToEnemy):
        self.distanceToEnemy = distanceToEnemy

    def run(self):
        if self.distanceToEnemy[0] < 15 and self.distanceToEnemy[1] < 15:
            return True
        else:
            return False
