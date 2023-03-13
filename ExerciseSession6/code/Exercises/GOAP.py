import sys
import copy
from vector import Vector2
from threading import Timer
from constants import *
from goalAndActions import *
from world import *


class GOAP(object):
    # EXERCISE 9
    def __init__(self, depth):
        # GOALS
        
        # ACTIONS FOR GOAL: KILL_GHOST
                
        # ACTIONS FOR GOAL: EAT_SUPERPELLETS

        return

    # EXERCISE 10
    def updateWorldState(self):
        return

    # EXERCISE 3
    def planAction(self, worldModel, maxDepth):
        # Create storage for world models at each depth, and
        # actions that correspond to them
        models = [None] * int(self.depth+1)
        actions = [None] * int(self.depth)
        
        # Set up the initial data
        models[0] = worldModel
        currentDepth = 0

        # Keep track of the best action
        bestAction = None
        bestValue = sys.maxsize

        # IMPLEMENT THE REST OF THE ALGORITHM BELOW
        # Iterate until we have completed all actions at depth 0

            # Calculate the discontentment value
            
            # Check if we're at maximum depth ...

                # If current value is best, store it
                    
                    # We're done at this depth, so drop back and ump to next iteration

            # ... otherwise, we need to try the next action, if there is one.

                # If there is an action, copy the current model ...

                # ... apply the action to the copy ...
                
                # ... and process it on the next iteration.

            # Otherwise we have no action to try, so we’re done at this level

                # Drop back to the next highest level

        # We've finished iterating, so return the result
    
        return

    # EXERCISE 11
    def updateActionsValues(self):
        return

    # EXERCISE 12
    # Method for checking if goal values have to change.
    def updateGoalsValues(self):
        return

    # EXERCISE 13
    def run(self):
        return