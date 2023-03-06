from xml.etree.ElementTree import TreeBuilder
from constants import *
from entity import *

class Transition(object):
    def __init__(self, start_state, target_state):
        self.start_state = start_state
        self.target_state = target_state

    # Tests for checking if state has to change
    def isTriggered(self, path_len=None, coordinates=None, timer=None):
        # SEEK
        if self.start_state == SEEK:
            if self.target_state.state == WANDER:
                return self.seek2wander(path_len)
        # WANDER
        if self.start_state == WANDER:
            if self.target_state.state == SEEK:
                return self.wander2seek(coordinates, timer)
            elif self.target_state.state == FLEE:
                return self.wander2flee(timer)
        # FLEE
        if self.start_state == FLEE:
            if self.target_state.state == SEEK:
                return self.flee2seek(coordinates)

    def seek2wander(self, path):
        if len(path) < 3:
            print("SEEK2WANDER")
            return True
        else:
            return False
    def wander2seek(self, coordinates, timer):
        if int(timer) > 2 and int(timer) <= 5:
            if coordinates[1] <= SCREENHEIGHT/2:
                print("WANDER2SEEK")
                return True
        return False
    def wander2flee(self, timer):
        if int(timer) > 5:
            print("WANDER2FLEE")
            return True
        else:
            return False
    def flee2seek(self, coordinates):
        if any([coordinates == (16,64),     # top-left
                coordinates == (416,64),    # top-right
                coordinates == (16,464),    # bot-left
                coordinates == (416,464)]): # bot-right
            print("FLEE2SEEK")
            return True
        else:
            return False
            

class State(object):
    def __init__(self, state):
        self.state = state 
        
    def getOtherStates(self, state1, state2):
        # SEEK
        if self.state == SEEK:
            self.wander = state1
            self.flee = state2
            self.seek2wander = Transition(self.state, self.wander)
        # WANDER
        if self.state == WANDER:
            self.seek = state1
            self.flee = state2
            self.wander2seek = Transition(self.state, self.seek)
            self.wander2flee = Transition(self.state, self.flee)
        # FLEE
        if self.state == FLEE:
            self.seek = state1
            self.wander = state2
            self.flee2seek = Transition(self.state, self.seek)
    # Return which transitions are possible from each state
    def getTransitions(self):
        if self.state == SEEK:
            return [self.seek2wander]
        if self.state == WANDER:
            return [self.wander2seek, self.wander2flee]
        if self.state == FLEE:
            return [self.flee2seek]
        


class StateMachine(object):
    def __init__(self, initial_state):
        # Holds a list of states for the machine
        self.seek = State(SEEK)
        self.wander = State(WANDER)
        self.flee = State(FLEE)
        
        self.seek.getOtherStates(self.wander, self.flee)
        self.wander.getOtherStates(self.seek, self.flee)
        self.flee.getOtherStates(self.seek, self.wander)

        # Holds the initial state
        if initial_state == SEEK:
            self.initialState = self.seek
        elif initial_state == WANDER:
            self.initialState = self.wander
        elif initial_state == FLEE:
            self.initialState = self.flee
        # Holds the current state
        self.currentState = self.initialState
        
        
    # Checks and applies transitions, returning a list of actions.
    def updateState(self, path_len=None, coordinates=None, timer=None):
        # Assume no transition is triggered 
        triggeredTransition = None
        print(timer)

        # Check through each transition and 
        # store the first one that triggers.
        for transition in self.currentState.getTransitions():
            if transition.isTriggered(path_len, coordinates, timer):
                triggeredTransition = transition
                break
        
        # Check if we have a transition to fire
        if triggeredTransition:
            # Find the triggered state
            targetState = triggeredTransition.target_state

            # Complete transition and return action list
            self.currentState = targetState
            print(path_len,timer)
            return self.currentState.state

        else:
            return self.currentState.state