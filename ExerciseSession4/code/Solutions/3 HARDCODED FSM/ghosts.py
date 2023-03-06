import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Ghost(Entity):
    def __init__(self, node, nodes, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        # self.directionMethod = self.wanderBiased
        self.pacman = pacman
        self.nodes = nodes
        self.speed = 80
        
        self.myState = SEEK
    
    def update(self, dt):
        self.goal = self.pacman.position
        Entity.update(self, dt)

    
