from xml.etree.ElementTree import TreeBuilder
from constants import *
from entity import *

class Transition(object):
    def __init__(self, start_state, target_state):
        self.start_state = start_state
        self.target_state = target_state

    # EXERCISE 8
    def seek2wander(self):
        return

    def wander2seek(self):
        return 
    def wander2flee(self):
        return

    def flee2seek(self):
        return
    
    # EXERCISE 9
    # Tests for checking if state has to change
    def isTriggered(self, path_len=None, coordinates=None, timer=None):
        # SEEK
        
        # WANDER
        
        # FLEE
        return
    
    # EXERCISE 10
    def getTargetState(self):
        return
            

class State(object):
    def __init__(self, state):
        self.state = state 

    # EXERCISE 12    
    def getOtherStates(self, state1, state2):
        # SEEK
        
        # WANDER
        
        # FLEE
        return
    
    # EXERCISE 13 
    # Return which transitions are possible from each state
    def getTransitions(self):
        return
        

class StateMachine(object):
    # EXERCISE 14
    def __init__(self):
        return
        
    # EXERCISE 15
    # Checks and applies transitions, returning a list of actions.
    def updateState(self, path_len=None, coordinates=None, timer=None):
        return