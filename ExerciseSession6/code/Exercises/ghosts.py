from argparse import Action
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from FSM import StateMachine
from random import choice
from behaviourTree import *

class Ghost(Entity):
    def __init__(self, node, nodes, pacman=None):
        Entity.__init__(self, node, nodes)
        self.name = GHOST
        self.color = WHITE
        self.goal = Vector2()
        self.speed = 80
        self.pacman = pacman
        self.enemy = self.pacman
        self.directionMethod = self.goalDirection

        self.freeze = False
        self.flag = False
        
    
    # def update(self, dt):
    #     self.behaviouralTree()
        
    #     if not self.freeze:
    #         self.timer += dt
    #         self.position += self.directions[self.direction]*self.speed*dt
            
    #         if self.overshotTarget():
    #             self.node = self.target
    #             directions = self.validDirections()
    #             direction = self.directionMethod(directions)
    #             self.target = self.getNewTarget(direction)
    #             if self.target is not self.node:
    #                 self.direction = direction
    #             else:
    #                 self.target = self.getNewTarget(self.direction)

    #             self.setPosition()
    #     else:
    #         pass

    def update(self, dt):
        self.goal = self.pacman.position
        Entity.update(self, dt)

    def freezeChar(self):
        self.freeze = True
        
    def setFlag(self):
        self.flag = True

    def behaviouralTree(self):
        myPosition = self.position
        enemyPosition = self.pacman.position
        distanceToEnemy = (abs(myPosition.x-enemyPosition.x), 
                           abs(myPosition.y-enemyPosition.y))
        isFlagSet = IsFlagSet(self)
        enemyFar = EnemyFar(distanceToEnemy)
        wander = Wander(self)
        firstSequence = Sequence([isFlagSet, enemyFar, wander])

        enemyNear = EnemyNear(distanceToEnemy, self.flag)
        goTopLeft = GoTopLeft(self)
        freeze = Freeze(self)
        secondSequence = Sequence([enemyNear, goTopLeft, freeze])

        top_node = Selector([firstSequence, secondSequence])
        top_node.run()
        print(top_node)