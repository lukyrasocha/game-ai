from vector import Vector2

# EXERCISE 2
class Task(object):
    def __init__(self):
        pass

    def run():
        return
       
# EXERCISE 3
class Selector(Task):
    def __init__(self, children):
        self.children = children 

    def run(self):
        for c in self.children:
            if c.run():
                return True
            return False

class Sequence(Task):
    def __init__(self) -> None:
        self.children = []

    def run(self):
        for c in self.children:
            if not c.run():
                return False
        return True
            
# EXERCISE 4
class EnemyFar(Task):
    def __init__(self, distanceToEnemy: Vector2):
        self.distanceToEnemy = distanceToEnemy
        self.threshold = 3

    def run(self):
        if self.distanceToEnemy.magnitude() > self.threshold:
            return True
        else:
            return False

# EXERCISE 5
class Wander(Task):
    def __init__(self, character):
        self.character = character
    
    def run(self):
        self.character.directionMethod =  self.character.wanderBiased
        return True

# EXERCISE 6
class EnemyNear(Task):
    def __init__(self, distanceToEnemy: Vector2):
        self.distanceToEnemy = distanceToEnemy
        self.threshold = 3

    def run(self):
        if self.distanceToEnemy.magnitude() > self.threshold:
            return True
        else:
            return False

# EXERCISE 8
class GoTopLeft(Task):
    pass



# EXERCISE 9
class Freeze(Task):
    pass
        

class IsFlagSet(Task):
    def __init__(self, character):
        self.character = character
    def run(self):
        if self.character.setFlag:
            return False
        else:
            return True