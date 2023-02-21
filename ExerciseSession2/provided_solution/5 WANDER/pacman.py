from random import uniform, randint
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
        self.last_update = 0
        self.WANDER_TYPE = 2
        self.ring_dist = 200
        self.ring_radius = 150

    def update(self, dt):	
        # self.follow_mouse()
        # self.acc = self.seek_and_arrive(pygame.mouse.get_pos())
        self.acc = self.wander_improved()
        self.vel += self.acc
        if self.vel.length() > self.speed:
            self.vel.scale_to_length(self.speed)
        self.position += self.vel
        if self.position.x > SCREENWIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = SCREENWIDTH
        if self.position.y > SCREENHEIGHT:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = SCREENHEIGHT

        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        self.direction = direction

    
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
        # desired
        pygame.draw.line(self.screen, 
                        RED, 
                        self.position, 
                        (self.position + self.desired * scale), 
                        5)
        if self.WANDER_TYPE == 1:
            pygame.draw.circle(self.screen, WHITE, (int(self.target.x), int(self.target.y)), 8)
        if self.WANDER_TYPE == 2:
            center = self.position + self.vel.normalize() * self.ring_dist
            pygame.draw.line(self.screen, WHITE, center, self.displacement, 5)
            pygame.draw.circle(self.screen, WHITE, (int(center.x), int(center.y)), self.ring_radius, 1)
        else:
            # approach radius
            pygame.draw.circle(self.screen, WHITE, pygame.mouse.get_pos(), APPROACH_RADIUS, 1)
        
    def wander(self):
        RAND_TARGET_TIME = 500
        self.WANDER_TYPE = 1
        # select random target every few sec
        now = pygame.time.get_ticks()   #returns time since pygame.init() was called
        if now - self.last_update > RAND_TARGET_TIME:
            self.last_update = now
            self.target = pygame.math.Vector2(randint(0, SCREENWIDTH), randint(0, SCREENHEIGHT))
        return self.seek(self.target)

    def wander_improved(self):
        self.WANDER_TYPE = 2
        future = self.position + self.vel.normalize() * self.ring_dist
        target = future + pygame.math.Vector2(self.ring_radius, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)