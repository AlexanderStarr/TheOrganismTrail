import random

DIRS = {'l': (-10, 0), 'r': (10, 0), 'u': (0, 10), 'd': (0, -10)}

class Bacteria:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.canGrow = {'l': True, 'r': True, 'u': True, 'd': True}

    def __repr__(self):
        return "Cell"

    def draw(self):
        return (self.x, self.y, 10, 10)

    def reproduce(self):
        direction = random.choice(DIRS.keys())
        coords = DIRS[direction]
        if self.canGrow[direction]:
            self.canGrow[direction] = False
            return (self.x + coords[0], self.y + coords[1])
        else:
            return False

    def canReproduce(self):
        return self.canGrow['l'] or self.canGrow['r'] or self.canGrow['u'] or self.canGrow['d']
    
