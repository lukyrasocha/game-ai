from argparse import Action
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from FSM import StateMachine
from random import choice
from behaviourTree import *

class Ghost(Entity):
    def __init__(self, node, nodes, pacman=None):
        Entity.__init__(self, node, nodes)
        self.name = GHOST
        self.color = WHITE
        self.goal = Vector2()
        self.speed = 80
        self.pacman = pacman
        self.enemy = self.pacman
    
    def update(self, dt):
        self.goal = self.pacman.position
        Entity.update(self, dt)



    # EXERCISE 10
    def behaviouralTree(self):
        return