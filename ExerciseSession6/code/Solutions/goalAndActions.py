import sys
import copy
from random import choice
from vector import Vector2
from threading import Timer
from constants import *

class Goal(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    # added in second part of exercise
    def getDiscontentment(self):
        return (self.value * self.value)
    def updateValue(self, newValue):
        self.value = newValue


class Action(object):
    def __init__(self, name):
        self.name = name
        self.value = 0
    
    def getGoalChange(self, goal):
        return

######
class FollowPathToTarget(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 5
    def getGoalChange(self, goal):
        if goal.name == KILL_GHOST:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        character.goal = character.enemy.position
        character.directionMethod = character.goalDirectionDij

class GoInSameQuadrant(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 4
    def getGoalChange(self, goal):
        if goal.name == KILL_GHOST:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        res = ()
        if character.enemyQuadrant == TOP_LEFT:
            res = (16,64)
        elif character.enemyQuadrant == TOP_RIGHT:
            res = (416,64)
        elif character.enemyQuadrant == BOT_LEFT:
            res = (16,464)
        elif character.enemyQuadrant == BOT_RIGHT:
            res = (416,464)
        character.goal = Vector2(res)

class Accelerate(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 2
    def getGoalChange(self, goal):
        if goal.name == KILL_GHOST:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        character.speed = 300

####
class VisitAnotherQuadrant(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 4
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        quads = [TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT]
        quads.remove(character.quadrant)
        quad = choice(quads)
        res = ()
        if quad == TOP_LEFT:
            res = (16,64)
        elif quad == TOP_RIGHT:
            res = (416,64)
        elif quad == BOT_LEFT:
            res = (16,464)
        elif quad == BOT_RIGHT:
            res = (416,464)
        character.goal = Vector2(res)
        return quad

class Wander(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 1
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        character.directionMethod = character.wanderBiased

class GoClosestCorner(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 2
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=1
    def exec(self, character):
        if character.quadrant == TOP_LEFT:
            res = (16,64)
        elif character.quadrant == TOP_RIGHT:
            res = (416,64)
        elif character.quadrant == BOT_LEFT:
            res = (16,464)
        elif character.quadrant == BOT_RIGHT:
            res = (416,464)
        character.goal = Vector2(res)

class Dummy(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 1
    def getGoalChange(self, goal):
        goal.value -= self.value
        