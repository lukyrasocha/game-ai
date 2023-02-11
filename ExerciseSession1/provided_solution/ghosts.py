import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Ghost(Entity):
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
    
    def update(self, dt):
        self.goal = self.pacman.position
        Entity.update(self, dt)
