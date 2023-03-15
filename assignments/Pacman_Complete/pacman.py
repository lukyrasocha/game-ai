import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from algorithms import dijkstra, astar, heuristic
from behaviourTree import *

class Pacman(Entity):
    def __init__(self, node, nodes):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.nodes = nodes
        

    def setGhosts(self, ghosts):
        self.ghosts = ghosts


    def get_dijsktra_distance(self, ghost):
        shortest_path, previous_nodes = dijkstra(self.nodes, self.node)
        
        for node in shortest_path:
            if node == ghost.node:
                return shortest_path[node]

    def avoidGhosts(self, directions):
        distances = []
        ds = []
        ghosts = []

        #blinky, pinky, inky, clyde

        #Find the closest ghost
        for ghost in self.ghosts:
            #vec = self.node.position - ghost.position
            #distances.append(vec.magnitudeSquared())
            ghosts.append(ghost)
            ds.append(len(astar(self.target, ghost.target, self.nodes, heuristic)))

        #closest_ghost = self.ghosts.ghosts[distances.index(min(distances))]
        #print("CLOSEST GHOST:")
        #print(closest_ghost.nickname)
        #try:
        #    print(len(astar(self.node, closest_ghost.node, self.nodes, heuristic)))
        #except:
        #    pass
        #print(self.get_dijsktra_distance(closest_ghost))
        print("="*50)
        print(ghosts[0].nickname, ds[0])
        print(ghosts[1].nickname, ds[1])
        print(ghosts[2].nickname, ds[2])
        print(ghosts[3].nickname, ds[3])

        closest_ghost = ghosts[ds.index(min(ds))]


        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - closest_ghost.position 
            distances.append(vec.magnitudeSquared())
        maxD = max(distances)
        
        #if (self.node.position - closest_ghost.position).magnitudeSquared() > maxD:
        #    print("OPPOSITE BETTER")
        #    print(self.direction)
        #    print(self.direction * -1)
            #return self.direction * -1
       #     self.reverseDirection()
            #return self.direction
            
        index = distances.index(maxD)
        print(directions[index])
        return directions[index]

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):	

        self.behaviouralTree()

        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt

        #directions = self.validDirections()
        #direction = self.avoidGhosts(directions)

        directions = self.validDirections()
        direction = self.directionMethod(directions)
        print(self.directionMethod)
        print(self.goal)

        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    def behaviouralTree(self):
        ghosts_nearby = GhostsNearby(5, self.node, self.ghosts, self.nodes)
        flee_from_ghosts = FleeFromGhosts(self.nodes, self, self.ghosts)
                           
        firstSequence = Sequence([ghosts_nearby, flee_from_ghosts])

        top_node = Selector([firstSequence])
        top_node.run()
