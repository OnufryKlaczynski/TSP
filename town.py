import math

class Town:

    def __init__(self, x, y, index):
        self.index = index
        self.x = x
        self.y = y

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y and self.index == other.index else False
    

    def __repr__(self):
        return f'Town x={self.x} y={self.y}'


    def __add__(self, other):

        return Town.distance(self, other)

    @staticmethod
    def distance(townA, townB):

        return math.sqrt((townA.x - townB.x)**2 + (townA.y - townB.y)**2)

