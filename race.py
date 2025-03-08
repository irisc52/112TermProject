
class Race:
    def __init__(self, course, distance, stroke, swimmer=None):
        self.swimmer = swimmer
        self.course = course
        self.distance = distance
        self.stroke = stroke
        self.laps = distance//25 if course == 'SCM' else distance//50
        self.fifties = distance // 50
        self.currSplit = ''
        self.splits = []
        self.lap = 1
        self.fifty = 1
    
        self.strategies = ['Go out aggressive',
                           'Hold pace better',
                           'Similar to past splits']
        self.selectedStrategy = None
        self.goalTime = ''
        
        #for IM
        self.bestStroke = None
        self.worstStroke = None
        
        #for mode 2 similar splits
        self.allRawSplits = []

    def __repr__(self):
        return f'{self.distance} {self.stroke} {self.course}'
    
    def addSplit(self, split):
        self.splits.append(float(split))
        self.currSplit = ''
    
    def addToAllSplits(self, split):
        self.allRawSplits.append(float(split))
        self.currSplit = ''
    
    def speeds(self, stroke): #speed is in pixels per step
        #assumptions: 30 steps per second, 24 pixels per "meter"
        speeds = []
        for split in self.splits:
            speeds.append((24*50)/(30*split))
        if stroke == 'BK':
            #difference of 60 pixels, aka 2.5 "meters"
            actualFirstFifty = speeds[0] / 50 * 47.5
            speeds.pop(0)
            speeds = [actualFirstFifty] + speeds
        return speeds
    
    def convertTimeToSplits(self, strategy):
        if ':' not in self.goalTime:
            minutes = 0
            seconds = self.goalTime
        else:
            minutes = self.goalTime[:self.goalTime.find(':')]
            seconds = self.goalTime[self.goalTime.find(':')+1:]
        minToSec = int(minutes)*60
        seconds = float(seconds)
        totalTime = minToSec + seconds
        if strategy == 'Go out aggressive':
            self.aggressiveSplits(totalTime)
        elif strategy == 'Hold pace better':
            self.holdPaceSplits(totalTime)
        elif self.stroke == 'IM':
            self.getIMSplits(self.bestStroke, self.worstStroke, totalTime)
    
    def getSimulatedTime(self):
        firstRace = self.allRawSplits[:self.fifties]
        secondRace = self.allRawSplits[self.fifties:self.fifties*2+1]
        thirdRace = self.allRawSplits[self.fifties*2:]
        for i in range(len(firstRace)):
            average = (firstRace[i] + secondRace[i] + thirdRace[i]) / 3
            self.splits.append(average)
    
    def aggressiveSplits(self, t):
        if self.distance == 50:
            self.splits.append(float(self.goalTime))
        elif self.distance == 100:
            if self.stroke == 'FL' or self.stroke == 'BR':
                firstFifty = t / 2 - 1.5
                secondFifty = t / 2 + 1.5
            elif self.stroke == 'FR' or self.stroke == 'BK':
                firstFifty = t / 2 - 1
                secondFifty = t / 2 + 1
            self.splits.append(firstFifty)
            self.splits.append(secondFifty)
        elif self.distance == 200:
            if self.stroke == 'FL' or self.stroke == 'BR':
                firstFifty = t/4 - 3.5
                secondFifty = t/4
                thirdFifty = t/4 + 1.5
                fourthFifty = t/4 + 2
            elif self.stroke == 'FR' or self.stroke == 'BR':
                firstFifty = t/4 - 3
                secondFifty = t/4
                thirdFifty = t/4 + 1.5
                fourthFifty = t/4 + 1.5
            self.splits.append(firstFifty)
            self.splits.append(secondFifty)
            self.splits.append(thirdFifty)
            self.splits.append(fourthFifty)
        
    def holdPaceSplits(self, t):
        if self.distance == 50:
            self.splits.append(float(self.goalTime))
        if self.distance == 100:
            if self.stroke == 'FL' or self.stroke == 'BR':
                firstFifty = t/2 - 1
                secondFifty = t/2 + 1
            elif self.stroke == 'FR' or self.stroke == 'BK':
                firstFifty = t/2 - 0.5
                secondFifty = t/2 + 0.5
            self.splits.append(firstFifty)
            self.splits.append(secondFifty)   
        elif self.distance == 200:
            if self.stroke == 'FL' or self.stroke == 'BR':
                firstFifty = t/4 - 2.5
                secondFifty = t/4
                thirdFifty = t/4 + 1.5
                fourthFifty = t/4 + 1
            elif self.stroke == 'FR' or self.stroke == 'BK':
                firstFifty = t/4 - 1.5
                secondFifty = t/4 + 0.5
                thirdFifty = t/4 + 0.5
                fourthFifty = t/4 + 0.5              
            self.splits.append(firstFifty)
            self.splits.append(secondFifty)
            self.splits.append(thirdFifty)
            self.splits.append(fourthFifty)

    def getIMSplits(self, best, worst, t):
        normalSplits = {'FL': t/4 - 5,
                        'BK': t/4 + 1,
                        'BR': t/4 + 6,
                        'FR': t/4 - 2}
        for stroke in normalSplits:
            if stroke == best:
                normalSplits[stroke] -= 1
            elif stroke == worst:
                normalSplits[stroke] += 1
        for stroke in normalSplits:
            self.splits.append(normalSplits[stroke])