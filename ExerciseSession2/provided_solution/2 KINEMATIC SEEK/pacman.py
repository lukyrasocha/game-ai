import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import uniform


class Pacman(object):
    def __init__(self, screen):
        self.name = PACMAN
        self.position = pygame.math.Vector2(200, 400)
        self.directions = {STOP:pygame.math.Vector2(), UP:pygame.math.Vector2(0,-1), DOWN:pygame.math.Vector2(0,1), LEFT:pygame.math.Vector2(-1,0), RIGHT:pygame.math.Vector2(1,0)}
        self.direction = STOP
        self.speed = 10
        self.radius = 10
        self.color = YELLOW

        self.direction = pygame.math.Vector2(self.speed, 0).rotate(uniform(0,360))
        self.velocity = Vector2()
        self.screen = screen

    def update(self, dt):	
        self.follow_mouse()
        self.direction += self.velocity
        if self.direction.length() > self.speed:
            self.direction.scale_to_length(self.speed)
        self.position += self.direction

        # self.position += self.directions[self.direction]*self.speed*dt
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
        p = self.position #no .asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    def follow_mouse(self):
        mpos = pygame.mouse.get_pos()
        mpos2 = (mpos[0]+1, mpos[1]+ 1)
        self.velocity = (mpos2 - self.position).normalize() * 0.2
        # normalize == make length 1 
        # unit vectors are usually used for representing direction 
        # and we can scale it to whatever the velocity is

    def draw_vectors(self):
        scale=25
        #direction vector
        pygame.draw.line(self.screen, 
                        YELLOW, 
                        self.position,
                        (self.position + self.direction * scale),
                        5) 