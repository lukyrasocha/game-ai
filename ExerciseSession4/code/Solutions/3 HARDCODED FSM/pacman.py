from asyncio.proactor_events import constants


import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.goal = Vector2()
        # self.directionMethod = self.goalDirection
        
        self.myState = FLEE

    def getGhostObject(self, ghost):
        self.ghost = ghost

    def update(self, dt):
        self.goal = self.ghost.position
        Entity.update(self, dt)