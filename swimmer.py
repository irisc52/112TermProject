from cmu_graphics import *
from helper import getRadiusEndpoint
import race

class Swimmer:
    def __init__(self, dimension, stroke, name, lane):
        self.lane = lane
        self.name = name
        self.headRadius = dimension/60
        self.color = 'blue'
        self.dir = -1 # right
        self.size = dimension / 50
        self.coveredDistance = 0 #do this in meters
        if stroke == 'BK':
            self.x, self.y = dimension / 8, dimension/4 + (lane-1)*dimension/12+ 0.5*dimension/12 #poolWidth
            self.startCapTheta = 290
            self.bodyTheta = -90
            self.armTheta = 140
            self.legTheta = 200
        else:
            self.startCapTheta = -20
            self.x, self.y = dimension / 20, dimension / 4 + (lane-1)*dimension/12+ 0.5*dimension/12 #poolWidth
            self.startCapTheta = 290
            self.armTheta = -75
            self.legTheta = 240
            self.bodyTheta = 150
        self.diving = True
        self.turning = False
        self.kickDirection = 1
        self.headDirection = 1
        self.relHeadPosition = 0
        self.armDirection = 1
        self.finished = False
        self.distanceCovered = 0
        self.centralized = False
        
    
    def reset(self, stroke, fifty):
        if stroke == 'FL' or stroke == 'IM' and fifty == 1:
            self.armTheta = 0
            self.legTheta = -165 + (self.dir+1)*0.5*180
        elif stroke != 'BR':
            self.armTheta = 180*self.dir
            self.legTheta = -165 + (self.dir+1)*0.5*180
        else:
            self.armTheta = 75*self.dir
            self.legTheta = 180
        self.diving = False

    
    def drawDive(self):
        bodyBackX, bodyBackY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta)
        bodyFrontX, bodyFrontY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta + 180)
        armStartX, armStartY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta + 180)
        armEndX, armEndY = getRadiusEndpoint(armStartX, armStartY, self.size, self.armTheta)
        drawLine(armStartX, armStartY, armEndX, armEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(armStartX, armStartY, self.size*0.4, fill='blue')
        drawCircle(armEndX, armEndY, self.size*0.4, fill='blue')
        legStartX, legStartY = bodyBackX, bodyBackY
        legEndX, legEndY = getRadiusEndpoint(legStartX, legStartY, self.size*1.25, self.legTheta)
        drawLine(legStartX, legStartY, legEndX, legEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(legStartX, legStartY, self.size*0.4, fill='blue')
        drawCircle(legEndX, legEndY, self.size*0.4, fill='blue')
        drawLine(bodyBackX, bodyBackY, bodyFrontX, bodyFrontY, lineWidth=self.size, fill='blue')
        drawCircle(bodyBackX, bodyBackY, self.size/2, fill='blue')
        drawCircle(bodyFrontX, bodyFrontY, self.size/2, fill='blue')
        headX, headY = getRadiusEndpoint(self.x, self.y, self.size*1.9, self.bodyTheta + 180)
        drawCircle(headX, headY, self.size/2, fill='blue')
        drawArc(headX, headY, self.size*1.05, self.size*1.05, self.startCapTheta, 180, fill='lightBlue')
        # drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        drawLine(armStartX, armStartY, armEndX, armEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(armStartX, armStartY, self.size*0.4, fill='blue')
        drawCircle(armEndX, armEndY, self.size*0.4, fill='blue')
        drawLine(legStartX, legStartY, legEndX, legEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(legStartX, legStartY, self.size*0.4, fill='blue')
        drawCircle(legEndX, legEndY, self.size*0.4, fill='blue')
    
    def drawTurn(self):
        bodyBackX, bodyBackY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta)
        bodyFrontX, bodyFrontY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta + 180)
        armStartX, armStartY = getRadiusEndpoint(self.x, self.y, self.size, self.bodyTheta + 180)
        armEndX, armEndY = getRadiusEndpoint(armStartX, armStartY, self.size, self.armTheta)
        drawLine(armStartX, armStartY, armEndX, armEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(armStartX, armStartY, self.size*0.4, fill='blue')
        drawCircle(armEndX, armEndY, self.size*0.4, fill='blue')
        legStartX, legStartY = bodyBackX, bodyBackY
        legEndX, legEndY = getRadiusEndpoint(legStartX, legStartY, self.size*1.25, self.legTheta)
        drawLine(legStartX, legStartY, legEndX, legEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(legStartX, legStartY, self.size*0.4, fill='blue')
        drawCircle(legEndX, legEndY, self.size*0.4, fill='blue')
        drawLine(bodyBackX, bodyBackY, bodyFrontX, bodyFrontY, lineWidth=self.size, fill='blue')
        drawCircle(bodyBackX, bodyBackY, self.size/2, fill='blue')
        drawCircle(bodyFrontX, bodyFrontY, self.size/2, fill='blue')
        headX, headY = getRadiusEndpoint(self.x, self.y, self.size*1.9, self.bodyTheta + 180)
        drawCircle(headX, headY, self.size/2, fill='blue')
        drawArc(headX, headY, self.size*1.05, self.size*1.05, -20, 180, fill='lightBlue')
        # drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        drawLine(armStartX, armStartY, armEndX, armEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(armStartX, armStartY, self.size*0.4, fill='blue')
        drawCircle(armEndX, armEndY, self.size*0.4, fill='blue')
        drawLine(legStartX, legStartY, legEndX, legEndY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(legStartX, legStartY, self.size*0.4, fill='blue')
        drawCircle(legEndX, legEndY, self.size*0.4, fill='blue')

    def drawFree(self):
        #draw first arm (behind)
        armLength = self.size
        endX, endY = getRadiusEndpoint(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, armLength, self.armTheta)
        drawLine(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size * 0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw first leg (behind)
        legLength = self.size * 1.25
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, legLength, self.legTheta)
        drawLine(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw torso and head
        drawLine(self.x - self.size, self.y, self.x + self.size, self.y, lineWidth = self.size, fill='blue')
        drawCircle(self.x - self.size, self.y, self.size//2, fill='blue')
        drawCircle(self.x + self.size, self.y, self.size//2, fill='blue')
        headPosition = self.y + self.relHeadPosition
        drawCircle(self.x - self.dir*(self.size*1.9), headPosition, self.size//2, fill='blue')
        #arc depends on if it's free or back (because it's the cap)
        drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        #draw second leg(in front)
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size), self.y, legLength, -self.legTheta)
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        drawLine(self.x + self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        #draw second arm (in front)
        endX, endY = getRadiusEndpoint(self.x - self.dir*self.size, self.y, armLength, self.armTheta + 180)
        drawLine(self.x - self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')

    def drawBack(self):
        #draw first arm (behind)
        armLength = self.size
        endX, endY = getRadiusEndpoint(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, armLength, self.armTheta)
        drawLine(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size * 0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw first leg (behind)
        legLength = self.size * 1.25
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, legLength, self.legTheta)
        drawLine(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw torso and head
        drawLine(self.x - self.size, self.y, self.x + self.size, self.y, lineWidth = self.size, fill='blue')
        drawCircle(self.x - self.size, self.y, self.size//2, fill='blue')
        drawCircle(self.x + self.size, self.y, self.size//2, fill='blue')
        headPosition = self.y + self.relHeadPosition
        drawCircle(self.x - self.dir*(self.size*1.9), headPosition, self.size//2, fill='blue')
        #arc depends on if it's free or back (because it's the cap)
        drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 150, 180, fill='lightBlue')
        #draw second leg(in front)
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size), self.y, legLength, -self.legTheta)
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        drawLine(self.x + self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        #draw second arm (in front)
        endX, endY = getRadiusEndpoint(self.x - self.dir*self.size, self.y, armLength, self.armTheta + 180)
        drawLine(self.x - self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')

    def drawFly(self):
        #draw first arm (behind)
        armLength = self.size
        endX, endY = getRadiusEndpoint(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, armLength, self.armTheta)
        drawLine(self.x - self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size * 0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw first leg (behind)
        legLength = self.size * 1.25
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, legLength, self.legTheta)
        drawLine(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw torso and head
        drawLine(self.x - self.size, self.y, self.x + self.size, self.y, lineWidth = self.size, fill='blue')
        drawCircle(self.x - self.size, self.y, self.size//2, fill='blue')
        drawCircle(self.x + self.size, self.y, self.size//2, fill='blue')
        headPosition = self.y + self.relHeadPosition
        drawCircle(self.x - self.dir*(self.size*1.9), headPosition, self.size//2, fill='blue')
        drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        #draw second leg(in front)
        endX, endY = getRadiusEndpoint(self.x + self.dir*(self.size), self.y, legLength, self.legTheta)
        drawLine(self.x + self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #draw second arm (in front)
        endX, endY = getRadiusEndpoint(self.x - self.dir*self.size, self.y, armLength, self.armTheta)
        drawLine(self.x - self.dir*self.size, self.y, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')

    def drawBreast(self):
        #arm
        armLength = self.size
        elbowX, elbowY = getRadiusEndpoint(self.x - self.dir*(self.size + self.size/5), self.y-self.size/5, armLength/2, self.armTheta)
        if self.dir == -1:
            endAngle = 0
        else:
            endAngle = 180
        endX, endY = getRadiusEndpoint(elbowX, elbowY, armLength/2, endAngle)
        drawLine(self.x - self.dir*(self.size + self.size/5), self.y-self.size/5, elbowX, elbowY, lineWidth = self.size*0.75, fill='blue')
        drawLine(elbowX, elbowY, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(elbowX, elbowY, self.size*0.4, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #leg
        legLength = self.size*1.25
        kneeX, kneeY = getRadiusEndpoint(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, legLength/2, self.legTheta)
        endX, endY = getRadiusEndpoint(kneeX, kneeY, legLength/2, 360-self.legTheta)
        drawLine(self.x + self.dir*(self.size + self.size/5), self.y - self.size/5, kneeX, kneeY, lineWidth = self.size*0.75, fill='blue')
        drawLine(kneeX, kneeY, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        drawCircle(kneeX, kneeY, self.size*0.4, fill='blue')
        #torso
        drawLine(self.x - self.size, self.y, self.x + self.size, self.y, lineWidth = self.size, fill='blue')
        drawCircle(self.x - self.size, self.y, self.size/2, fill='blue')
        drawCircle(self.x + self.size, self.y, self.size/2, fill='blue')
        #head
        headPosition = self.y + self.relHeadPosition
        drawCircle(self.x - self.dir*(self.size*1.9), self.y + self.relHeadPosition, self.size/2, fill='blue')
        drawArc(self.x - self.dir*(self.size*1.9), headPosition, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        #front arm
        elbowX, elbowY = getRadiusEndpoint(self.x - self.dir*(self.size), self.y, armLength/2, self.armTheta)
        endX, endY = getRadiusEndpoint(elbowX, elbowY, armLength/2, endAngle)
        drawLine(self.x - self.dir*self.size, self.y, elbowX, elbowY, lineWidth = self.size*0.75, fill='blue')
        drawLine(elbowX, elbowY, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(elbowX, elbowY, self.size*0.4, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        #front leg
        kneeX, kneeY = getRadiusEndpoint(self.x + self.dir*(self.size), self.y, legLength/2, self.legTheta)
        endX, endY = getRadiusEndpoint(kneeX, kneeY, legLength/2, 360-self.legTheta)
        drawLine(self.x + self.dir*(self.size), self.y, kneeX, kneeY, lineWidth = self.size*0.75, fill='blue')
        drawLine(kneeX, kneeY, endX, endY, lineWidth = self.size*0.75, fill='blue')
        drawCircle(endX, endY, self.size*0.4, fill='blue')
        drawCircle(kneeX, kneeY, self.size*0.4, fill='blue')

    def drawIM(self, race):
        if race.fifty == 1:
            self.drawFly()
        elif race.fifty == 2:
            self.drawBack()
        elif race.fifty == 3:
            self.drawBreast()
        else:
            self.drawFree()
        #this just draws one of the above based on where in the race the swimmer is
    
    def drawName(self):
        drawLabel(f'{self.name}', self.x + self.dir*5*self.size, self.y)
    
    def drawFinishPose(self):
        #draw head and body
        drawCircle(self.x, self.y - self.size*1.9, self.size/2, fill='blue')
        drawArc(self.x, self.y - self.size*1.9, self.size*1.05, self.size*1.05, 0, 180, fill='lightBlue')
        drawLine(self.x, self.y - self.size, self.x, self.y + self.size, lineWidth = self.size, fill='blue')
        drawCircle(self.x, self.y - self.size, self.size/2, fill='blue')
        drawCircle(self.x, self.y + self.size, self.size/2, fill='blue')
        #draw arms
        armLength = self.size
        for i in range(2):
            endX, endY = getRadiusEndpoint(self.x - self.size/5 + 2*i*self.size/5, self.y - self.size/2, armLength, 115 - i*50)
            drawLine(self.x - self.size/5 + 2*i*self.size/5, self.y - self.size/2, endX, endY, lineWidth = self.size*0.75, fill='blue')
            drawCircle(self.x - self.size/5 + 2*i*self.size/5, self.y - self.size/2, self.size*0.4, fill='blue')
            drawCircle(endX, endY, self.size*0.4, fill='blue')
        legLength = self.size * 1.25
        for i in range(2):
            drawLine(self.x - self.size/5 + 2*i*self.size/5, self.y + self.size, 
                     self.x - self.size/5 + 2*i*self.size/5, self.y + self.size + legLength, lineWidth = self.size*0.75, fill='blue')
            drawCircle(self.x - self.size/5 + 2*i*self.size/5, self.y + self.size, self.size*0.4, fill='blue')
            drawCircle(self.x - self.size/5 + 2*i*self.size/5, self.y + self.size + legLength, self.size*0.4, fill='blue')
        
        
    def step(self, paused, stroke, race, timer, x):
        if not paused:
            if self.finished:
                self.x = x
            elif self.diving and stroke != 'BK':
                self.stepDive()
            elif self.diving and stroke == 'BK':
                self.stepBackDive()
            elif self.turning:
                self.stepTurn()
            elif stroke == 'FR' or stroke == 'BK' or stroke == 'FL':
                self.stepFrBkFl(stroke)
            elif stroke == 'BR':
                self.stepBreast()
            elif stroke == 'IM':
                if race.fifty == 3:
                    self.stepBreast()
                else:
                    self.stepFrBkFl(stroke)
    
    def stepBackDive(self):
        if self.armTheta > 0:
            self.armTheta -= 8
        if self.startCapTheta > 150:
            self.startCapTheta -= 8
        if self.bodyTheta > -180:
            self.bodyTheta -= 8
        elif self.legTheta > 180:
            self.legTheta -= 8
        
    
    def stepDive(self):
        if self.legTheta > self.bodyTheta:
            self.legTheta -= 5
        if self.armTheta < self.bodyTheta - 180:
            self.armTheta += 5
        if self.bodyTheta < 180:
            self.bodyTheta += 1

    def stepTurn(self):
        if (self.bodyTheta >= 180 and self.dir == 1) or (self.bodyTheta <= 0 and self.dir == -1):
            self.turning = False
        elif self.dir == -1 and self.bodyTheta > 0:
            self.bodyTheta -= 25
        elif self.dir == 1 and self.bodyTheta < 180:
            self.bodyTheta += 25
        if self.dir == -1:
            self.legTheta -= 15
        else:
            self.legTheta -= 15
    
    def stepFrBkFl(self, stroke):
        if stroke == 'FR' or stroke == 'BK':
            armSpeed = 5
            legSpeed = 4
        else:
            armSpeed = 8
            legSpeed = 3
        if self.dir == 1 and (abs(self.legTheta) > 15):
            self.kickDirection = -self.kickDirection
        elif (self.dir == -1) and (self.legTheta < -200 or self.legTheta > -160):
            self.kickDirection = -self.kickDirection
        self.legTheta -= self.kickDirection*legSpeed #magic number, will change
        self.armTheta += armSpeed*self.dir #magic number, will change
        self.relHeadPosition += 0.2*self.headDirection #magic number, will change
        if self.relHeadPosition >= 1 or self.relHeadPosition <= -1:
            self.headDirection = -self.headDirection
        if self.dir == 1 and (abs(self.legTheta) > 15):
            self.kickDirection = -self.kickDirection
        elif (self.dir == -1) and (self.legTheta < -200 or self.legTheta > -160):
            self.kickDirection = -self.kickDirection
        self.legTheta -= self.kickDirection*legSpeed #magic number, will change
        self.armTheta += armSpeed*self.dir #magic number, will change
        self.relHeadPosition += 0.2*self.headDirection #magic number, will change
        if self.relHeadPosition >= 1 or self.relHeadPosition <= -1:
            self.headDirection = -self.headDirection

    def stepBreast(self):
        armSpeed = -3
        legSpeed = 4
        if (((self.legTheta > 270 or self.legTheta < 180) and self.dir == -1) or
            ((self.legTheta > 0 or self.legTheta < -90) and self.dir == 1)):
            self.kickDirection = -self.kickDirection
        if (((self.armTheta < -90 or self.armTheta > -30) and self.dir == -1) or
            (self.dir == 1 and (self.armTheta > -90 or self.armTheta < -150))):
            self.armDirection = -self.armDirection
        self.armTheta += armSpeed*self.armDirection
        self.legTheta += legSpeed*self.kickDirection