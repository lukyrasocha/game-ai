import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from random import choice
from algorithms import dijkstra_or_a_star

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.goal = Vector2()
        self.directionMethod = self.goalDirection

    def getGhostObject(self, ghost):
        self.ghost = ghost

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(max(distances))
        return directions[index]

    def update(self, dt):
        self.goal = self.ghost.position
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    #############
    # Executes Dijkstra from Ghost's previous node as start 
    # to pacman's target node as target.
    def getDijkstraPath(self, directions):
        lastGhostNode = self.ghost.target
        lastGhostNode = self.nodes.getPixelsFromNode(lastGhostNode)
        pacmanTarget = self.target
        pacmanTarget = self.nodes.getPixelsFromNode(pacmanTarget)

        # previous_nodes, shortest_path = dijkstra(self.nodes, pacmanTarget)
        previous_nodes, shortest_path = dijkstra_or_a_star(self.nodes, pacmanTarget, a_star=True)
        path = []
        node = lastGhostNode
        while node != pacmanTarget:
            path.append(node)
            node = previous_nodes[node]
        path.append(pacmanTarget)
        path.reverse()
        # print(path)
        return path

    # Chooses direction in which to turn based on the dijkstra
    # returned path
    def goalDirectionDij(self, directions):
        path = self.getDijkstraPath(directions)
        print(path)
        pacmanTarget = self.target
        pacmanTarget = self.nodes.getPixelsFromNode(pacmanTarget)
        path.append(pacmanTarget)
        nextGhostNode = path[1]
        if pacmanTarget[0] > nextGhostNode[0] and 2 in directions : #left
            return 2
        if pacmanTarget[0] < nextGhostNode[0] and -2 in directions : #right
            return -2
        if pacmanTarget[1] > nextGhostNode[1] and 1 in directions : #up
            return 1
        if pacmanTarget[1] < nextGhostNode[1] and -1 in directions : #down
            return -1
        else:
            print(self.ghost.direction)
            print(directions)
            if -1 * self.ghost.direction in directions:
                return -1 * self.ghost.direction
            else: 
                return choice(directions)
        
        # up 1, down -1, left 2, right -2