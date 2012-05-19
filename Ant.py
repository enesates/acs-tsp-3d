class Ant(object):
    def __init__(self, antId):
        self.id = antId
        self.tour = []
        self.tourLength = 0
        self.visitedCity = []