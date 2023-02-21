import pygame
from pygame.locals import *
from vector import Vector2
from constants import *



class Ghost(object):
    def __init__(self):
        self.name = PACMAN
        self.position = Vector2(400, 100)
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = RED

    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        # direction = self.getValidKey()
        # self.direction = direction

    
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

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

