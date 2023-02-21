from random import uniform
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *



class Pacman(object):
    def __init__(self, screen):
        self.name = PACMAN
        self.position = pygame.math.Vector2(200, 400)
        self.directions = {STOP:pygame.math.Vector2(), UP:pygame.math.Vector2(0,-1), DOWN:pygame.math.Vector2(0,1), LEFT:pygame.math.Vector2(-1,0), RIGHT:pygame.math.Vector2(1,0)}
        self.direction = STOP
        self.speed = 10 
        self.radius = 10
        self.color = YELLOW

        self.vel = pygame.math.Vector2(self.speed, 0).rotate(uniform(0,360))
        self.acc = Vector2()
        self.screen = screen

    def update(self, dt):	
        # self.follow_mouse()
        self.acc = self.seek(pygame.mouse.get_pos())
        self.vel += self.acc 
        if self.vel.length() > self.speed:
            self.vel.scale_to_length(self.speed)
        self.position += self.vel 

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
        p = self.position
        pygame.draw.circle(screen, self.color, p, self.radius)

    def follow_mouse(self):
        mpos = pygame.mouse.get_pos()
        mpos2 = (mpos[0]+1, mpos[1]+ 1)
        self.acc = (mpos2 - self.position).normalize() * 0.2
        # normalize == make length 1 
        # unit vectors are usually used for representing direction 
        # and we can scale it to whatever the acceleration is

    def seek(self, target):
        self.desired = (target-self.position).normalize() * self.speed
        steer = (self.desired - self.vel)
        STEERING_FORCE = 0.5
        if steer.length() > STEERING_FORCE:
            steer.scale_to_length(STEERING_FORCE)
        return steer

    def draw_vectors(self):
        scale=25
        #vel vector
        pygame.draw.line(self.screen, 
                        YELLOW, 
                        self.position,
                        (self.position + self.vel * scale),
                        5) 
        # desired
        pygame.draw.line(self.screen, 
                        RED, 
                        self.position, 
                        (self.position + self.desired * scale), 
                        5)