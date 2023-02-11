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
        self.directionMethod = self.fleeDirection

    #def update(self, dt):	
    #    self.position += self.directions[self.direction]*self.speed*dt
    #    direction = self.getValidKey()
    #    if self.overshotTarget():
    #            self.node = self.target
    #            self.target = self.getNewTarget(direction)
    #            if self.target is not self.node:
    #                self.direction = direction
    #            else: # so then if you have o----x-----x the pacman would continue to the right most x without stopping at the first x
    #                self.target = self.getNewTarget(self.direction)

    #            if self.target is self.node:
    #                self.direction = STOP
    #            self.setPosition()
    #    else: 
    #        if self.oppositeDirection(direction):
    #            self.reverseDirection()

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




