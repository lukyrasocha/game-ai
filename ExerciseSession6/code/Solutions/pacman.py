from math import sqrt
import pygame
from pygame.locals import *
from vector import Vector2
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
        self.speed = 100
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
        self.goal = self.ghost.position
        self.speed = 150
        action = self.execGOAP(dt)
        action.exec(self)
        self.update_timers(dt)
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

    def update_timers(self, dt):
        self.GOAPtimer += dt
        self.killedTimer += dt
        self.timer += dt

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet
        return None

    # EXERCISE 14
    def updateKillFlag(self):
        if self.killedFlag:
            if int(self.killedTimer) >= 5:
                self.killedFlag = False
        else:
            distanceToEnemy = (abs(self.position.x-self.enemy.position.x), 
                            abs(self.position.y-self.enemy.position.y))
            if distanceToEnemy[0] <= 15 and distanceToEnemy[1] <= 15:
                # Set flag to true
                self.killedFlag = True
                # Restart timer from 0, so that it counts how long
                # it has been since enemy was killed.
                self.killedTimer = 0

    def updateQuadrant(self, relevantPosition):
        inLeftHalf = True if relevantPosition.x <= (SCREENWIDTH/2) else False
        inTopHalf = True if relevantPosition.y <= (SCREENHEIGHT/2) else False

        if inTopHalf:
            return TOP_LEFT if inLeftHalf else TOP_RIGHT
        else:
            return BOT_LEFT if inLeftHalf else BOT_RIGHT
        
    def execGOAP(self, dt):
        print("________________________")
        self.updateKillFlag()
        self.quadrant = self.updateQuadrant(self.position)
        self.enemyQuadrant = self.updateQuadrant(self.enemy.position)
        nextAction = self.GOAP.run(self.killedFlag, 
                                   self.quadrant,
                                   self.enemyQuadrant,
                                   dt)
        print("NEXT ACTION:         ", nextAction)
        return nextAction