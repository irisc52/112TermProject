from cmu_graphics import *

class Pool:
    def __init__(self, dimension, course, lanes):
        self.lanes = lanes
        self.waterColor = 'skyBlue'
        self.laneLineColor = 'red'
        self.laneWidth = dimension / 12
        self.laneLineWidth = dimension / 80
        if course == 'SCM':
            self.length = dimension * 0.75
        else:
            self.length = dimension * 1.5
        self.topLeftX = dimension / 7
        self.topRightX = self.topLeftX + self.length - 50
        self.topLeftY = dimension / 4
        self.topRightY = self.topLeftY
        self.margin = 50 / self.lanes #how much the right and left move for each successive lane (for 3d effect)
        self.blockMargin = 50
        self.blockHeight = 30
            