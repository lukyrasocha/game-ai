import sys
import copy
from vector import Vector2
from threading import Timer
from constants import *

# EXERCISE 4
class Goal(object):
    def __init__(self, name, value):
        # TO IMPLEMENT
        pass
    
    def getDiscontentment(self):
        # TO IMPLEMENT
        return
    
    def updateValue(self, newValue):
        # TO IMPLEMENT
        return


class Action(object):
    # EXERCISE 5
    def __init__(self, name):
        # TO IMPLEMENT
        pass
    
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
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

class GoInSameQuadrant(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 4
    def getGoalChange(self, goal):
        if goal.name == KILL_GHOST:
            goal.value -= self.value
        else:
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

class Accelerate(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 2
    def getGoalChange(self, goal):
        if goal.name == KILL_GHOST:
            goal.value -= self.value
        else:
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

####
class VisitAnotherQuadrant(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 4
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

class Wander(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 10
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

class GoClosestCorner(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 2
    def getGoalChange(self, goal):
        if goal.name == EAT_SUPERPELLETS:
            goal.value -= self.value
        else:
            goal.value +=100
    # EXERCISE 16
    def exec(self):
        # TO IMPLEMENT
        return

class Dummy(Action):
    def __init__(self, name):
        Action.__init__(self, name)
        self.value = 1
    def getGoalChange(self, goal):
        goal.value -= self.value
        