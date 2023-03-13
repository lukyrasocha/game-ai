from vector import Vector2

class Task(object):
    def __init__(self):
        # Holds a list of the children (if any) of this task
        self.children
    
    # Always terminates with either success (True) or failure (False)
    def run(self):
        return 

class Selector(Task):
    def __init__(self, children):
        self.children = children
    
    def run(self):
        for c in self.children:
            if c.run():
                return True
        return False

class Sequence(Task):
    def __init__(self, children):
        self.children = children 
    
    def run(self):
        for c in self.children:
            print(c)
            if not c.run():
                return False
        return True

class EnemyFar(Task):
    def __init__(self, distanceToEnemy):
        self.distanceToEnemy = distanceToEnemy

    def run(self):
        if self.distanceToEnemy[0] >= 15 and self.distanceToEnemy[1] >= 15:
            return True
        else:
            return False

class Wander(Task):
    def __init__(self, character):
        self.character = character
    def run(self):
        self.character.directionMethod = self.character.wanderBiased
        return True

class EnemyNear(Task):
    def __init__(self, distanceToEnemy, flag):
        self.distanceToEnemy = distanceToEnemy
        self.flag = flag

    def run(self):
        if self.distanceToEnemy[0] < 15 and self.distanceToEnemy[1] < 15:
            return True
        else:
            if self.flag:
                return True
            else:
                return False

class GoTopLeft(Task):
    def __init__(self, character):
        self.character = character
    def run(self):
        self.character.setFlag()
        self.character.directionMethod = self.character.goalDirection
        self.character.goal = Vector2(16,64)
        return True

class Freeze(Task):
    def __init__(self, character):
        self.character = character
    def run(self):
        if self.character.position == Vector2(16,64):
            self.character.freezeChar()
        return True
        

class IsFlagSet(Task):
    def __init__(self, character):
        self.character = character
    def run(self):
        if self.character.flag:
            return False
        else:
            return True