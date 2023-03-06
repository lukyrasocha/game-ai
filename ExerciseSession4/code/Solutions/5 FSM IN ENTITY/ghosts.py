import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from FSM import StateMachine
from random import choice

class Ghost(Entity):
    def __init__(self, node, nodes, pacman=None):
        Entity.__init__(self, node, nodes)
        self.name = GHOST
        self.color = WHITE
        self.goal = Vector2()
        self.speed = 80
        
        self.pacman = pacman
        
    
    def update(self, dt):
        self.goal = self.pacman.position
        Entity.update(self, dt)

    
    