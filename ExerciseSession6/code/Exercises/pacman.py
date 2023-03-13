from math import sqrt
from turtle import screensize
import pygame
from pygame.locals import *
from vector import Vector2
from random import choice
from constants import *
from entity import Entity
from algorithms import dijkstra, print_result, dijkstra_or_a_star
from GOAP import GOAP

class Pacman(Entity):
    def __init__(self, node, nodes):
        Entity.__init__(self, node, nodes)
        self.name = PACMAN
        self.color = YELLOW
        self.goal = Vector2()
        self.speed = 150
        self.directionMethod = self.wanderBiased
        self.collideRadius = 5

        # self.myState = FLEE
        
        self.start_dt = self.timer
        self.cornerReached =False

        self.GOAP = GOAP(depth=3)
        self.GOAPtimer = 0
        self.killedFlag = False 
        self.killedTimer = 0
        self.quadrant = None
        self.enemyQuadrant = None


    def getGhostObject(self, ghost):
        self.ghost = ghost
        self.enemy = self.ghost
        
    def update(self, dt):
        self.execGOAP(dt)
        self.goal = self.ghost.position
        self.GOAPtimer += dt
        self.killedTimer += dt
        self.timer += dt
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()
        
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet
        return None

    def updateKillFlag(self):
        return
    
    def updateQuadrant(self, relevantPosition):
        return
        
    def execGOAP(self, dt):
        print("________________________")
        self.updateKillFlag()
        self.quadrant = self.updateQuadrant(self.position)
        self.enemyQuadrant = self.updateQuadrant(self.enemy.position)
        nextAction = self.GOAP.run(self.killedFlag, 
                                   self.quadrant,
                                   self.enemyQuadrant,
                                   dt)
        print(nextAction)
        # exit()

    # EXERCISE 16
    def execFollowTarget(self):
        return

    def execAccelerate(self):
        return

    def execGoTargetQuadrant(self):
        return

    def execGoDifferentQuadrant(self):
        return

    def execWander(self):
        return

    def execCorner(self):
        return