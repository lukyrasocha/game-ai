import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from FSM import StateMachine
from random import choice

class Ghost(Entity):
    def __init__(self, node, nodes, pacman=None):
        Entity.__init__(self, node, nodes)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.wanderBiased
        self.pacman = pacman
        self.nodes = nodes
        self.speed = 80
        
        
        # FSM   
        # Added constants in "constants.py" file
        self.states = [SEEK, FLEE, WANDER]
        self.myState = SEEK
        self.timer = 0
        self.FSM = StateMachine()
        self.init_path = [[], [], [], []]
        self.path = self.init_path
        self.seek_or_flee = True    # seek=True, flee=False
        self.old_state = 0

        self.FSM_decision
    
    def update(self, dt):
        self.goal = self.pacman.position
        self.timer += dt
        self.advancedFSM()
        Entity.update(self, dt)

    
    def FSM_decision(self):
        if self.myState == SEEK: 
            self.directionMethod = self.goalDirectionDij
        elif self.myState == FLEE:
            self.seek_or_flee = False
            self.directionMethod = self.goalDirection
        elif self.myState == WANDER:
            self.directionMethod = self.wanderBiased
        else:
            self.myState = choice(self.states)

    # SEEK <--> WANDER --> FLEE
    #  ^---------------------'
    # SEEKtoWANDER = if target is < 2 nodes away
    # WANDERtoSEEK = if character is in top-left half in 2 < x <= 5 seconds
    # WANDERtoFLEE = after 5 seconds
    # FLEEtoSEEK = if character hits one of the corners
    def advancedFSM(self):
        position = self.position
        position = (int(position.x), int(position.y))
        new_state = self.FSM.updateState(self.path, coordinates=position, timer=int(self.timer))
        # print(new_state)
        if new_state == SEEK: 
            self.speed = 80
            self.directionMethod = self.goalDirectionDij
        elif new_state == FLEE:
            self.speed = 180
            self.seek_or_flee = False
            self.directionMethod = self.goalDirection
        elif new_state == WANDER:
            self.speed = 180
            self.directionMethod = self.wanderBiased
        else:
            new_state = choice(self.states)
        if self.old_state != new_state:
            print(True)
            self.timer = 0
        self.old_state = new_state
        self.path = self.init_path