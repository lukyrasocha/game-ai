from random import uniform
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *



class Pacman(object):
    def __init__(self, screen, ghost):
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
        self.ghost = ghost

    def update(self, dt):	
        self.vel = self.ghost.vel
        self.acc = self.ghost.acc
        if self.position.x > SCREENWIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = SCREENWIDTH
        if self.position.y > SCREENHEIGHT:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = SCREENHEIGHT

    
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

    def seek_and_arrive(self, target):
        APPROACH_RADIUS = 50
        self.desired = (target-self.position)
        dist = self.desired.length()    #we get the distance before normalizing the desired
        self.desired.normalize_ip() # ip = in place 
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * self.speed
        else:
            self.desired *= self.speed
        steer = (self.desired - self.vel)
        STEERING_FORCE = 0.5
        if steer.length() > STEERING_FORCE:
            steer.scale_to_length(STEERING_FORCE)
        return steer

    def draw_vectors(self):
        scale=25
        APPROACH_RADIUS = 50
        #vel vector
        pygame.draw.line(self.screen, 
                        YELLOW, 
                        self.position,
                        (self.position + self.vel * scale),
                        5) 
        # # desired
        # pygame.draw.line(self.screen, 
        #                 RED, 
        #                 self.position, 
        #                 (self.position + self.desired * scale), 
        #                 5)
        # # approach radius
        # pygame.draw.circle(self.screen, WHITE, pygame.mouse.get_pos(), APPROACH_RADIUS, 1)