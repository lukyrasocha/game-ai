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