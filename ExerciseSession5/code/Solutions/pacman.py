import pygame
from pygame.locals import *
from vector import Vector2
from random import choice
from constants import *
from entity import Entity
from algorithms import dijkstra, print_result, dijkstra_or_a_star

class Pacman(Entity):
    def __init__(self, node, nodes):
        Entity.__init__(self, node, nodes)
        self.name = PACMAN
        self.color = YELLOW
        self.goal = Vector2()
        self.speed = 150

        self.myState = FLEE

    def getGhostObject(self, ghost):
        self.ghost = ghost
        self.enemy = self.ghost
        
    def update(self, dt):
        self.goal = self.ghost.position
        Entity.update(self, dt)

    #############
    # Executes Dijkstra from Ghost's previous node as start 
    # to pacman's target node as target.
    def getDijkstraPath(self, directions):
        lastGhostNode = self.ghost.target
        lastGhostNode = self.nodes.getPixelsFromNode(lastGhostNode)
        pacmanTarget = self.target
        pacmanTarget = self.nodes.getPixelsFromNode(pacmanTarget)

        # previous_nodes, shortest_path = dijkstra(self.nodes, ghostTarget)
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
        ghostTarget = self.target
        ghostTarget = self.nodes.getPixelsFromNode(ghostTarget)
        path.append(ghostTarget)
        self.path = path
        nextGhostNode = path[1]
        if ghostTarget[0] > nextGhostNode[0] and 2 in directions : #left
            return 2
        if ghostTarget[0] < nextGhostNode[0] and -2 in directions : #right
            return -2
        if ghostTarget[1] > nextGhostNode[1] and 1 in directions : #up
            return 1
        if ghostTarget[1] < nextGhostNode[1] and -1 in directions : #down
            return -1
        else:
            if -1 * self.ghost.direction in directions:
                return -1 * self.ghost.direction
            else: 
                return choice(directions)
        
        # up 1, down -1, left 2, right -2