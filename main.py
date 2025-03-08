from cmu_graphics import *

import math
import pool
import swimmer
import race
import instructions
from helper import distance
from helper import almostEqual


def onAppStart(app):
    app.width, app.height = 800, 800
    app.homescreen = True
    app.instructions = False
    app.instructionsText = instructions.Instructions(app.width)
    app.getNumSwimmers = False
    app.numSwimmers = ''
    app.createSwimmers = False
    app.prepRace = False
    app.prepMode2 = False
    app.selectedMode = None
    app.selectedCourse = None
    app.selectedDistance = None
    app.selectedStroke = None
    app.buttonR = app.width*0.04
    app.paused = True
    app.racing = False
    app.direction = 1 #swimming right
    app.screenLeft = 0
    app.screenRight = app.screenLeft + app.width
    app.margin = app.width / 10 #margin to left of pool
    app.swimmerLane = 0
    app.diving = True
    app.playbackSpeed = 4
    app.timer = 0
    app.buttons = getButtons(app)
    app.strategyButtons = getStrategyButtons(app)
    app.validRaces = getValidRaces(app)
    app.bestWorstStrokes = getBestWorstStrokeButtons(app)
    app.invalidRace = False
    app.raceFinished = False
    app.swimmers = []
    app.races = []
    app.currSwimmer = 0 #the current swimmer getting info for
    app.currSwimmerName = ''
    url = 'https://drive.google.com/uc?id=1-_uWuigzt_E8_lbS_IO6IV1svCLcGNkt'
    #sound is from the NYT simulations (Relive the Biggest Little Swims in Paris)
    app.sound = Sound(url)

def onKeyPress(app, key):
    if app.homescreen:
        if (key == 'space' and 
             app.selectedMode != None and app.selectedCourse != None and app.selectedDistance != None and app.selectedStroke != None):
            if (app.selectedDistance, app.selectedStroke) not in app.validRaces:
                app.invalidRace = True
            else:
                app.race = race.Race(app.selectedCourse, app.selectedDistance, app.selectedStroke)
                app.pool = pool.Pool(app.width, app.selectedCourse, 8)
                app.homescreen = False
                app.getNumSwimmers = True
        if app.invalidRace and key == 'r':
            app.selectedDistance, app.selectedStroke = None, None
            app.invalidRace = False
    elif app.instructions:
        if key == 'b':
            app.instructions = False
            app.homescreen = True
    elif app.getNumSwimmers:
        if key == 'space' and 1 <= int(app.numSwimmers) <= 8:
            app.numSwimmers = int(app.numSwimmers)
            app.getNumSwimmers = False
            app.createSwimmers = True
        elif key.isdigit():
            app.numSwimmers += key
        elif key == 'backspace' and len(app.numSwimmers) > 0:
            app.numSwimmers = app.numSwimmers[:-1]
    elif app.createSwimmers:
        if key == 'backspace' and len(app.currSwimmerName) > 0:
            app.currSwimmerName = app.currSwimmerName[:-1]
        elif key == '+' and len(app.currSwimmerName) > 0:
            app.currSwimmerName = app.currSwimmerName.upper()
            app.swimmers.append(swimmer.Swimmer(app.width, app.selectedStroke, app.currSwimmerName, app.currSwimmer + 1))
            app.races.append(race.Race(app.selectedCourse, app.selectedDistance, app.selectedStroke, app.currSwimmer))
            app.currSwimmerName = ''
            app.currSwimmer += 1
        elif key == 'space' and len(app.swimmers) == app.numSwimmers:
            app.createSwimmers = False
            app.currSwimmer = 0
            app.prepRace = True
        elif key.isalpha() and len(key) == 1:
            app.currSwimmerName += key
    elif app.prepRace:
        if app.selectedMode == 1:
            if key.isdigit() or (key == '.' and '.' not in app.races[app.currSwimmer].currSplit):
                app.races[app.currSwimmer].currSplit += key
            elif key == 'backspace' and len(app.races[app.currSwimmer].currSplit) >0:
                app.races[app.currSwimmer].currSplit = app.races[app.currSwimmer].currSplit[:-1]
            elif (key == 'n' and app.races[app.currSwimmer].currSplit != '' and 
                  len(app.races[app.currSwimmer].splits) < app.races[app.currSwimmer].fifties):
                app.races[app.currSwimmer].addSplit(app.races[app.currSwimmer].currSplit)
            elif key == 'b' and len(app.races[app.currSwimmer].splits) > 0:
                app.races[app.currSwimmer].splits.pop()
                app.races[app.currSwimmer].currSplit = ''
            elif (key == '+' and len(app.races[app.currSwimmer].splits) == app.races[app.currSwimmer].fifties and 
                  app.currSwimmer + 1 < app.numSwimmers):
                app.currSwimmer += 1
            elif (key == 'space' and len(app.races[app.currSwimmer].splits) == app.race.fifties and
                  app.currSwimmer + 1 == app.numSwimmers):
                app.prepRace = False
                app.racing = True
                app.currSwimmer = 0
        elif app.selectedMode == 2: 
            if key == '+' and app.races[app.currSwimmer].selectedStrategy != None and app.currSwimmer + 1 < app.numSwimmers:
                app.currSwimmer +=1
            elif (key == '+' and app.selectedStroke == 'IM' and 
                  app.races[app.currSwimmer].bestStroke != None and
                  app.races[app.currSwimmer].worstStroke != None and
                  app.currSwimmer + 1 < app.numSwimmers):
                app.currSwimmer+= 1
            if key == 'space' and app.races[-1].selectedStrategy != None:
                app.prepRace = False
                app.prepMode2 = True
                app.currSwimmer = 0
            elif (key == 'space' and app.selectedStroke == 'IM' and
                  app.races[-1].bestStroke != None and
                  app.races[-1].bestStroke != None):
                app.prepRace = False
                app.prepMode2 = True
                app.currSwimmer = 0
    elif app.prepMode2: #and app.selectedStroke != 'IM':
        if app.races[app.currSwimmer].selectedStrategy in app.race.strategies[:2] or app.selectedStroke == 'IM':
            if (key.isdigit() or 
                (key == ':' and ':' not in app.races[app.currSwimmer].currSplit) or
                (key == '.' and '.' not in app.races[app.currSwimmer].currSplit)):
                    app.races[app.currSwimmer].goalTime += key
            elif key == 'backspace' and len(app.races[app.currSwimmer].goalTime) > 0:
                app.races[app.currSwimmer].goalTime = app.races[app.currSwimmer].goalTime[:-1]
            elif key == '+' and app.races[app.currSwimmer].goalTime != '' and app.currSwimmer + 1 < app.numSwimmers:
                app.races[app.currSwimmer].convertTimeToSplits(app.races[app.currSwimmer].selectedStrategy)
                app.currSwimmer += 1
            elif key == 'space' and app.races[-1].goalTime != '':
                app.races[app.currSwimmer].convertTimeToSplits(app.races[-1].selectedStrategy)
                app.prepMode2 = False
                app.racing = True
                app.currSwimmer = None
        else:
            if key.isdigit() or (key == '.' and '.' not in app.races[app.currSwimmer].currSplit):
                app.races[app.currSwimmer].currSplit += key
            elif key == 'backspace' and len(app.races[app.currSwimmer].currSplit) > 0:
                app.races[app.currSwimmer].currSplit = app.races[app.currSwimmer].currSplit[:-1]
            elif key == 'n' and app.races[app.currSwimmer].currSplit != '':
                app.races[app.currSwimmer].addToAllSplits(app.races[app.currSwimmer].currSplit)
            elif key == 'b' and len(app.races[app.currSwimmer].allRawSplits) > 0:
                app.races[app.currSwimmer].allRawSplits.pop()
                app.races[app.currSwimmer].currSplit = ''
            elif (key == '+' and len(app.races[app.currSwimmer].allRawSplits) == app.races[app.currSwimmer].fifties*3
                  and app.currSwimmer +1 < app.numSwimmers):
                app.races[app.currSwimmer].getSimulatedTime()
                app.currSwimmer+= 1
            elif key == 'space' and len(app.races[-1].allRawSplits) == app.races[-1].fifties*3: #??
                app.races[app.currSwimmer].getSimulatedTime()
                app.prepMode2 = False
                app.racing = True
                app.currSwimmer = None
    elif app.racing:
        if key == 'p' and not app.raceFinished:
            app.paused = not app.paused
            app.sound.play(loop=True)
    elif app.raceFinished:
        if key == 'right':
            if app.currSwimmer == None:
                app.currSwimmer = 0
            elif app.currSwimmer + 1 < app.numSwimmers:
                app.currSwimmer +=1
        elif key == 'left' and app.currSwimmer != None:
            if app.currSwimmer == 0:
                app.currSwimmer = None
            else:
                app.currSwimmer -= 1
        if key == 'r':
            resetApp(app)
            

def onMousePress(app, mouseX, mouseY):
    if app.homescreen:
        for x, y, value, category in app.buttons:
            if value == '?' and distance(mouseX, mouseY, x, y) <= app.buttonR:
                app.homescreen = False
                app.instructions = True
            if distance(mouseX, mouseY, x, y) <= app.buttonR:
                if category == 'mode':
                    app.selectedMode = value
                elif category == 'course':
                    app.selectedCourse = value
                elif category == 'distance':
                    app.selectedDistance = value
                elif category == 'stroke':
                    app.selectedStroke = value
    elif app.prepRace and app.selectedStroke == 'IM' and app.selectedMode == 2:
        for x, y, stroke in app.bestWorstStrokes:
            if distance(mouseX, mouseY, x, y) <= app.width*0.1:
                if app.races[app.currSwimmer].bestStroke == None:
                    app.races[app.currSwimmer].bestStroke = stroke
                    break
                elif app.races[app.currSwimmer].worstStroke == None:
                    app.races[app.currSwimmer].worstStroke = stroke
                    break
    elif app.selectedMode == 2 and app.prepRace:
        for x, y, strategy in app.strategyButtons:
            if distance(mouseX, mouseY, x, y) <= app.width/25:
                app.races[app.currSwimmer].selectedStrategy = strategy

def redrawAll(app):
    if app.homescreen:
        drawHomescreen(app)
    elif app.getNumSwimmers:
        drawGetNumSwimmers(app)
    elif app.createSwimmers and app.currSwimmer <= app.numSwimmers:
        createSwimmers(app)
    elif app.instructions:
        app.instructionsText.write()
    elif app.prepRace and app.currSwimmer <= app.numSwimmers:
        drawRacePrep(app)
    elif app.prepMode2:
        drawMoreMode2(app)
    elif app.raceFinished:
        app.sound.pause()
        drawFinishScreen(app)
    elif app.racing:
        secondsTens = '0' if app.timer%60 < 10 else ''
        font='monospace'
        drawLabel(f'{app.selectedDistance} {app.selectedStroke}', app.width*0.25, app.height*0.1, size=25, font=font, bold=True)
        drawRect(app.width*0.2, app.height*0.15, app.width*0.1, app.height*0.05, border='black', fill=None, align='center')
        drawLabel(f'{int(app.timer//60)}:{secondsTens}{app.timer%60:.1f}', app.width*0.2, app.height*0.15, font=font, size=16)
        drawLabel(f'Lap {app.race.lap} of {app.race.laps}', app.width*0.35, app.height*0.15, font=font, size=16)
        drawLabel(f'Race visualization shown at {app.playbackSpeed}x speed', app.width*0.5, app.height*0.22, size=16, font=font)
        drawPool(app)
        i = 0
        for swimmer in app.swimmers:
            if swimmer.centralized and not swimmer.finished:
                swimmer.drawName()
            if swimmer.finished:
                if app.selectedDistance == 50 and app.selectedCourse == 'LCM':
                    swimmer.x = app.width - app.margin
                swimmer.drawFinishPose()
            elif swimmer.diving:
                swimmer.drawDive()
            elif swimmer.turning:
                swimmer.drawTurn()
            elif app.selectedStroke == 'FR':
                swimmer.drawFree()
            elif app.selectedStroke == 'BK':
                swimmer.drawBack()
            elif app.selectedStroke == 'FL':
                swimmer.drawFly()
            elif app.selectedStroke == 'BR':
                swimmer.drawBreast()
            elif app.selectedStroke == 'IM':
                swimmer.drawIM(app.races[i])
            i+= 1
        drawExtraWater(app)
        if app.paused:
            drawRect(app.width/2, app.height/2, app.width*0.5, app.height*0.10, align='center', fill='lightGrey')
            drawLabel('Press p to start/resume the race!!', app.width/2, app.height/2, size=16, font=font)
        

def drawHomescreen(app):
    font = 'monospace'
    modes, courses, distances, strokes = [1, 2], ['LCM', 'SCM'], [50, 100, 200], ['FR', 'BK', 'BR', 'FL', 'IM']
    drawRect(0, 0, app.width, app.height, fill='lightBlue')
    drawLabel('Welcome To..', app.width/2, app.height*0.1, font=font, bold=True, size=16)
    drawLabel('THE SWIMULATOR', app.width/2, app.height*0.15, size=25, font=font, bold=True)
    drawLabel('Select Mode:',  app.width/2, app.height*0.25, font=font, size=16, bold=True)
    drawCircle(app.width*0.9, app.height*0.1, app.buttonR, fill='lightGrey')
    drawLabel('?', app.width*0.9, app.height*0.1, font=font, size=20)
    for l in range(len(modes)):
        if app.selectedMode == modes[l]:
            fill = 'lightGreen'
        else: fill='lightGrey'
        drawCircle( + app.width*(0.40+l*0.20), app.height*0.35, app.buttonR, fill=fill)
        drawLabel(modes[l],  + app.width*(0.40+l*0.20), app.height*0.35, font=font)
    drawLabel('Select Race and Course:',  + app.width/2, app.height*0.45, font=font, size=16, bold=True)
    for k in range(len(courses)):
        if app.selectedCourse == courses[k]:
            fill = 'lightGreen'
        else: fill = 'lightGrey'
        drawCircle( + app.width*(0.35+k*0.3), app.height*0.55, app.buttonR, fill=fill)
        drawLabel(courses[k],  + app.width*(0.35+k*0.3), app.height*0.55, font=font)
    for i in range(len(distances)):
        if app.selectedDistance == distances[i]:
            fill='lightGreen'
        else:
            fill='lightGrey'
        drawCircle( + app.width*(0.3+i*0.20), app.height*0.65, app.buttonR, fill=fill)
        drawLabel(f'{distances[i]}',  + app.width*(0.3+i*0.2), app.height*0.65, font=font)
    for j in range(len(strokes)):
        if app.selectedStroke == strokes[j]:
            fill = 'lightGreen'
        else: fill='lightGrey'
        drawCircle( + app.width*(0.2+j*0.15), app.height*0.75, app.buttonR, fill=fill)
        drawLabel(strokes[j],  + app.width*(0.2+j*0.15), app.height*0.75, font=font)
    drawRect( + app.width/2, app.height*0.9, 
            app.width*0.45, app.height*0.1, align='center', fill='blue')
    drawLabel('Press Space to Begin',  + app.width/2, app.height*0.9, size=20, fill='white', font=font, bold=True)
    if app.invalidRace:
        drawRect( + app.width*0.5, app.height*0.5, 
                 app.width*0.9, app.height*0.1, fill='red', align='center')
        drawLabel(f'Invalid Race: {app.selectedDistance} {app.selectedStroke}. Press r to choose another!', 
                   + app.width*0.5, app.height*0.5, size=16, fill='white', font=font, bold=True)

def drawGetNumSwimmers(app):
    font='monospace'
    drawLabel('How many swimmers in your race?', app.width/2, app.height*0.2, size=20, font=font)
    drawLabel('Enter a number from 1 to 8', app.width/2, app.height*0.25, size=16, font=font, italic=True)
    drawRect(app.width/2, app.height*0.4, app.width*.15, app.height*0.1, align='center', fill='lightGrey')
    drawLabel(app.numSwimmers, app.width/2, app.height*0.4, size=20, font=font)
    drawLabel('Press space to continue', app.width/2, app.height*0.75, size=16, font=font)

def createSwimmers(app):
    font='monospace'
    if app.currSwimmer >= app.numSwimmers:
        drawLabel('All done! Press space to continue', app.width/2, app.height/2, size=20, font=font)
    else:
        drawLabel(f'Enter the name of swimmer {app.currSwimmer+1}', app.width/2, app.height*0.2, size=20, font=font)
        drawRect(app.width/2, app.height*0.5, app.width*0.30, app.height*0.1, align='center', fill='lightGrey')
        drawLabel(app.currSwimmerName, app.width/2, app.height*0.5, size=16, font=font)
        drawLabel('Press + to go to the next swimmer', app.width/2, app.height*0.75, size=16, font=font)
        drawLabel('Press space when finished with all', app.width/2, app.height*0.85, size=16, font=font)
    

def drawRacePrep(app):
    if app.selectedMode == 1:
        drawMode1(app)
    else:
        drawMode2(app)

def drawMode1(app): #directly simulating based on given splits
    font = 'monospace'
    drawLabel(f'Enter splits (up to the hundredths) for {app.swimmers[app.currSwimmer].name}', app.width/2, app.height*0.15, size=20, font=font)
    drawLabel("Press n to go to the next split", app.width/2, app.height*0.20, font=font)
    drawLabel('Press b to go back to previous split', app.width/2, app.height*0.25, font=font)
    drawLabel('Press + to go to the next swimmer', app.width/2, app.height*0.30, font=font)
    drawLabel('Press space when finished', app.width/2, app.height*0.85, size=20, font=font)
    for fifty in range(app.races[app.currSwimmer].fifties):
        if fifty < len(app.races[app.currSwimmer].splits):
            fill='lightGreen'
        elif fifty == len(app.races[app.currSwimmer].splits):
            fill='yellow'
        else:
            fill='lightGrey'
        drawRect(app.width*(0.25 + 0.5*(fifty%2)), app.height*(0.40+0.3*(fifty//2)),
                 app.width*0.25, app.height*0.15, align='center', fill=fill)
        if len(app.races[app.currSwimmer].splits) > fifty: #the current fifty, not 50...confusing
            drawLabel(app.races[app.currSwimmer].splits[fifty], app.width*(0.25 + 0.5*(fifty%2)), app.height*(0.40+0.3*(fifty//2)), font=font)
        elif len(app.races[app.currSwimmer].splits) == fifty:
            drawLabel(app.races[app.currSwimmer].currSplit, app.width*(0.25 + 0.5*(fifty%2)), app.height*(0.40+0.3*(fifty//2)), font=font)

def drawMode2(app):
    font= 'monospace'
    if app.selectedStroke != 'IM':
        drawLabel(f'Pick a Race Strategy for {app.swimmers[app.currSwimmer].name}', app.width/2, app.height*0.2, size=20, font=font)
        for i in range(3):
            if app.races[app.currSwimmer].selectedStrategy == app.races[app.currSwimmer].strategies[i]:
                fill='lightGreen'
            else:
                fill='lightGrey'
            drawCircle(app.width/4, app.height*(0.3+i*0.15), app.width/25, fill=fill)
            drawLabel(f'{i+1}', app.width/4, app.height*(0.3+i*0.15), font=font, size=20)
            if app.races[app.currSwimmer].selectedStrategy == app.races[app.currSwimmer].strategies[i]:
                bold=True
            else: 
                bold = False
            drawLabel(f'{app.races[app.currSwimmer].strategies[i]}', app.width/3, app.height*(0.3+i*0.15), font=font, size=16, align='left', bold=bold)
    else:
        drawLabel(f"Pick {app.swimmers[app.currSwimmer].name}'s (1) best stroke (2) worst stroke", app.width/2, app.height*0.2, size=20, font=font)
        strokes = ['FL', 'BK', 'BR', 'FR'] # not including IM because this is IM
        for i in range(4):
            if app.races[app.currSwimmer].bestStroke == strokes[i]:
                fill='lightGreen'
            elif app.races[app.currSwimmer].worstStroke == strokes[i]:
                fill='lightCoral'
            else:
                fill='lightGrey'
            drawCircle(app.width*(0.25 + 0.5*(i%2)), app.height*(0.40+0.3*(i//2)), app.width*0.1, fill=fill)
            drawLabel(f'{strokes[i]}', app.width*(0.25 + 0.5*(i%2)), app.height*(0.40+0.3*(i//2)), size=20, font=font)
    drawLabel('Press + to go to the next swimmer', app.width/2, app.height*0.9, font=font, size=16)
    drawLabel('Pres space when finished', app.width/2, app.height*0.95, size=16, font=font)

def drawMoreMode2(app):
    if app.selectedStroke == 'IM':
        drawAgOrPaceMode2(app)
    elif app.races[app.currSwimmer].selectedStrategy == 'Go out aggressive' or app.races[app.currSwimmer].selectedStrategy == 'Hold pace better':
         drawAgOrPaceMode2(app) #just takes in a goal time and splits it itself
    else:
         drawSimilarSplitsMode2(app) #takes in past splits and bases new splits based on it
    pass

def drawAgOrPaceMode2(app):
    font='monospace'
    drawLabel(f'Enter goal time for {app.swimmers[app.currSwimmer].name}:', app.width/2, app.height/4, font=font, size=20)
    drawRect(app.width/2, app.height/3, app.width*0.25, app.height*0.10, align='center', fill='lightGrey')
    drawLabel(app.races[app.currSwimmer].goalTime, app.width/2, app.height/3, font=font, size=20)
    drawLabel('Press + to go to the next swimmer', app.width/2, app.height*0.9, font=font, size=16)
    drawLabel('Press space when finished', app.width/2, app.height*0.95, font=font, size=16)

def drawSimilarSplitsMode2(app):
    font='monospace'
    fifties = app.races[app.currSwimmer].fifties
    drawLabel(f'{app.swimmers[app.currSwimmer].name}', app.width/2, app.height*0.1, size=20, font=font)
    drawLabel('Enter splits for three past races with similar times', app.width/2, app.height*0.13, size=16, font=font)
    drawLabel('Press n to go to the next split, b to go back', app.width/2, app.height*0.16, font=font)
    for race in range(3):
        for fifty in range(fifties):
            if len(app.races[app.currSwimmer].allRawSplits) > fifties*race+fifty:
                fill='lightGreen'
            elif len(app.races[app.currSwimmer].allRawSplits) == fifties*race+fifty:
                fill='yellow'
            else:
                fill='lightGrey'
            drawLabel(f'{race + 1}', app.width*0.1, app.height*0.25 + race*app.height*0.25, size=25, font=font)
            drawRect(app.width*0.20 + fifty*app.width*0.20, app.height*0.25 + race*app.height*0.25,
                     app.width*0.15, app.height*0.10, fill=fill, align='center')
            if len(app.races[app.currSwimmer].allRawSplits) > fifties*race+fifty:
                drawLabel(app.races[app.currSwimmer].allRawSplits[fifties*race+fifty], app.width*0.20 + fifty*app.width*0.20, 
                          app.height*0.25 + race*app.height*0.25, font=font, size=16)
            elif len(app.races[app.currSwimmer].allRawSplits) == fifties*race+fifty:
                drawLabel(app.races[app.currSwimmer].currSplit, app.width*0.20 + fifty*app.width*0.20, 
                          app.height*0.25 + race*app.height*0.25, font=font, size=16)
    drawLabel('Press + to go to the next swimmer', app.width/2, app.height*0.9, size=16, font=font)
    drawLabel('Press space when finished', app.width/2, app.height*0.95, size=16, font=font)

def drawPool(app):
    laneWidth = app.pool.laneWidth
    laneLineWidth = app.pool.laneLineWidth
    poolLength = app.pool.length
    fifteenMeter = 0.45*app.width 
    for lane in range(app.pool.lanes):
        drawRect(app.screenLeft + app.margin/2, app.height//4 + lane*laneWidth + laneWidth/2, app.width/30, app.height/30, 
                 fill='grey', align = 'center') # block 
        drawRect(app.screenLeft + app.margin, app.height/4 + lane*laneWidth, poolLength, laneWidth, fill='skyBlue')
        drawRect(app.screenLeft + app.margin, app.height/4 + lane*laneWidth, poolLength, laneLineWidth, fill='red')
        drawRect(app.screenLeft + app.margin + fifteenMeter, app.height/4+lane*laneWidth, app.height/80, laneLineWidth, fill='gold')
        drawRect(app.screenLeft + app.margin + + poolLength - fifteenMeter, app.height/4+lane*laneWidth, app.height/80, laneLineWidth, fill='gold')
        drawLabel(f'{lane+1}', app.screenLeft + app.margin*1.25, app.height//4 + lane*laneWidth + laneWidth/2, font='montserrat')
    drawRect(app.screenLeft + app.margin, app.height/4 + app.pool.lanes*app.pool.laneWidth, poolLength, laneLineWidth, fill='red')
    drawRect(app.screenLeft + app.margin + fifteenMeter, app.height/4 + app.pool.lanes*laneWidth, app.height/80, laneLineWidth, fill='gold')
    drawRect(app.screenLeft + app.margin + poolLength - fifteenMeter, app.height/4 + app.pool.lanes*laneWidth, app.height/80, laneLineWidth, fill='gold')

def drawExtraWater(app):
    for lane in range(app.pool.lanes):
        drawRect(app.screenLeft + app.margin, app.height/4 + lane*app.pool.laneWidth + 0.5*app.pool.laneWidth, 
                 app.pool.length, app.pool.laneWidth*0.5, fill='skyBlue', opacity=50)

def drawFinishScreen(app):
    drawRect(0, 0, app.width, app.height, fill='lightBlue')
    font='monospace'
    drawLabel('RESULTS', app.width/2, app.height*0.2, size=20, font=font)
    rawFinalTimes = [sum(app.races[i].splits) for i in range(len(app.swimmers))]
    ties = dict()
    for i in range(len(rawFinalTimes)):
        time = rawFinalTimes[i]
        if rawFinalTimes.count(time) > 1:
            ties[time] = ties.get(time, []) + [app.swimmers[i].name]
    sortedTimes = sorted(rawFinalTimes)
    secondsTens = []
    for time in rawFinalTimes:
        if time%60 < 10:
            secondsTens.append('0')
        else:
            secondsTens.append('')
    finalTimes = []
    for i in range(len(rawFinalTimes)):
        time = rawFinalTimes[i]
        st = secondsTens[i]
        cleanedTime = f'{int(time//60)}:{st}{time%60:.2f}'
        finalTimes.append(cleanedTime)
    for i in range(len(sortedTimes)):
        j = rawFinalTimes.index(sortedTimes[i])
        if sortedTimes[i] in ties:
            k = sortedTimes.index(sortedTimes[i])
            currSwimmer = ties[sortedTimes[i]][-1]
            ties[sortedTimes[i]].pop()
        else:
            k = i
            currSwimmer = app.swimmers[j].name
        cleanedTime = finalTimes[j]
        drawLabel(f'{k + 1}     {currSwimmer}     {cleanedTime}', 
                  app.width/2, app.height*(0.25+0.05*i), size=16, font=font)
        if i == 0:
            drawLine(app.width*0.25, app.height*(0.225), app.width*0.75, app.height*(0.225))
        drawLine(app.width*0.25, app.height*(0.275 + 0.05*i), app.width*0.75, app.height*(0.275 + 0.05*i))
    drawLine(app.width*0.25, app.height*0.225, app.width*0.25, app.height*(0.225+0.05*len(sortedTimes)))
    drawLine(app.width*0.75, app.height*0.225, app.width*0.75, app.height*(0.225+0.05*len(sortedTimes)))
    drawLabel('Press the left and right arrows to see split analysis', app.width/2, app.height*0.85,
              size=16, font=font)
    if app.currSwimmer != None:
        drawRect(0, 0, app.width, app.height, fill='lightBlue')
        drawLabel(f'{app.swimmers[app.currSwimmer].name}', app.width/2, app.height*0.2, size=25, font=font)
        for i in range(len(app.races[app.currSwimmer].splits)):
            drawLabel(f'Lap {i + 1}: {app.races[app.currSwimmer].splits[i]:.2f}',
                      app.width/2, app.height*(0.35+0.05*i), size=16, font=font, align='right')
            if i > 0:
                if app.races[app.currSwimmer].splits[i] > app.races[app.currSwimmer].splits[i-1]:
                    sign = '+'
                    color = 'red'
                else:
                    sign = ''
                    color = 'green'
                drawLabel(f' {sign}{app.races[app.currSwimmer].splits[i]-app.races[app.currSwimmer].splits[i-1]:.2f}', 
                      app.width/1.9, app.height*(0.35+0.05*i), size=16, font=font, fill=color, align='left')
        if app.selectedStroke != 'IM' and app.selectedDistance > 50:
            drawLabel(f'Extracted first {len(app.races[app.currSwimmer].splits)*50//2}: {sum(app.races[app.currSwimmer].splits[:len(app.races[app.currSwimmer].splits)//2]):.2f}',
                        app.width/2, app.height*0.7, size=16, font=font)
            pace = sum(app.races[app.currSwimmer].splits) / len(app.races[app.currSwimmer].splits)
            drawLabel(f'Average Pace: {pace:.2f}', app.width/2, app.height*0.8, size=16, font=font)
    drawLabel('Press r to reset', app.width/2, app.height*0.90, size=16, font=font)


def onStep(app):
    positions = [swimmer.x for swimmer in app.swimmers]
    distCovered = [swimmer.distanceCovered for swimmer in app.swimmers]
    stillSwimming = []
    for swimmer in app.swimmers:
        if not swimmer.finished:
            stillSwimming.append(swimmer.name)
    distCovered = [swimmer.distanceCovered for swimmer in app.swimmers]
    if len(distCovered) == 1:
        leadSwimmer = lastSwimmer = 0
    else:
        leadSwimmer = None
        lastSwimmer = None
        for i in range(len(distCovered)):
            if leadSwimmer == None or distCovered[i] > distCovered[leadSwimmer]:
                leadSwimmer = i
            if lastSwimmer == None or distCovered[i] < distCovered[lastSwimmer]:
                lastSwimmer = i
    if not app.paused:
        if stillSwimming == []:
            app.racing = False
            app.raceFinished = True
            app.currSwimmer = None
            app.paused = True
        else:
            takeStep(app, leadSwimmer, lastSwimmer) #lead and last swimmer index


def takeStep(app, leadSwimmer, lastSwimmer):
    leadSwimmerSpeeds = app.races[leadSwimmer].speeds(app.selectedStroke)
    i = 0
    app.timer += (1/app.stepsPerSecond) * app.playbackSpeed
    for swimmer in app.swimmers:
        swimmer.step(app.paused, app.selectedStroke, app.races[i], app.timer, app.margin*1.5)
        swimmerSpeeds = app.races[i].speeds(app.selectedStroke)
        swimmer.distanceCovered += (1/app.stepsPerSecond) * app.playbackSpeed * swimmerSpeeds[app.races[i].fifty-1]
        app.screenRight = app.screenLeft + app.width
        if app.screenLeft + app.margin*3 < swimmer.x < app.screenRight- app.margin*3:
            swimmer.centralized = True
        if swimmer.x >= app.screenLeft + app.margin*2 and swimmer.diving:
            swimmer.diving = False
            swimmer.reset(app.selectedStroke, app.races[i].fifty)
        if ((app.screenLeft + app.margin + app.pool.length - 4*swimmer.size < swimmer.x + swimmer.headRadius and swimmer.dir == -1 or
            app.screenLeft + app.margin + 4*swimmer.size > swimmer.x - swimmer.headRadius and swimmer.dir == 1) and 
            app.races[i].lap != app.races[i].laps):
            swimmer.turning = True
        if (app.screenLeft + app.margin + app.pool.length <= app.swimmers[leadSwimmer].x + swimmer.headRadius and app.direction == 1 or
            app.screenLeft + app.margin > app.swimmers[leadSwimmer].x - swimmer.headRadius and app.direction == -1):
            app.direction = -app.direction
            app.swimmers[leadSwimmer].dir *= -1
            app.swimmers[leadSwimmer].turning = False
            app.swimmers[leadSwimmer].reset(app.selectedStroke, app.races[leadSwimmer].fifty)
            if app.swimmers[leadSwimmer].dir == 1: 
                if ((app.selectedStroke == 'BR') or 
                    app.selectedStroke == 'IM' and app.races[leadSwimmer].fifty == 3):
                    app.swimmers[leadSwimmer].legTheta = 0
                    app.swimmers[leadSwimmer].armTheta = -105               
                else:
                    app.swimmers[leadSwimmer].legTheta = 15 
            else: 
                if ((app.selectedStroke == 'BR') or 
                    app.selectedStroke == 'IM' and app.races[leadSwimmer].fifty == 2):
                    app.swimmers[leadSwimmer].legTheta = 180
                    app.swimmers[leadSwimmer].armTheta = -75
                else:
                    app.swimmers[leadSwimmer].legTheta = -165 
                    app.swimmers[leadSwimmer].armTheta = -75
            if app.races[leadSwimmer].lap == app.races[leadSwimmer].laps:
                print(leadSwimmer, 'hi')
                app.swimmers[leadSwimmer].finished = True
                if app.selectedDistance == 50:
                    swimmer.x = app.screenLeft + app.margin + app.pool.length - app.margin*1.5
                else:
                    swimmer.x = app.margin*1.5
                i+= 1
                j = 0
                for swimmer in app.swimmers:
                    if almostEqual(sum(app.races[j].splits), sum(app.races[leadSwimmer].splits)):
                        print(j, leadSwimmer, 'hello')
                        swimmer.finished = True
                    j += 1
                continue  
            if app.races[leadSwimmer].lap != app.races[leadSwimmer].laps:
                if app.races[leadSwimmer].lap % 2 == 0 and app.selectedCourse == 'SCM':
                    app.races[leadSwimmer].fifty += 1
                elif app.selectedCourse == 'LCM':
                    app.races[leadSwimmer].fifty += 1
                app.races[leadSwimmer].lap += 1
                app.race.lap += 1
        if i != leadSwimmer and ((app.screenLeft + app.margin + app.pool.length <= swimmer.x + swimmer.headRadius and swimmer.dir == -1 or
            app.screenLeft + app.margin > swimmer.x + swimmer.headRadius and swimmer.dir == 1)):
            swimmer.turning = False
            swimmer.dir = -swimmer.dir
            swimmer.reset(app.selectedStroke, app.races[i].fifty)
            if swimmer.dir == 1: 
                if ((app.selectedStroke == 'BR') or 
                    app.selectedStroke == 'IM' and app.races[i].fifty == 3):
                    swimmer.legTheta = 0
                    swimmer.armTheta = -105               
                else:
                    swimmer.legTheta = 15 
            else: 
                if ((app.selectedStroke == 'BR') or 
                    app.selectedStroke == 'IM' and app.races[i].fifty == 2):
                    swimmer.legTheta = 180
                    swimmer.armTheta = -75
                else:
                    swimmer.legTheta = -165 
                    swimmer.armTheta = -75
            if app.races[i].lap == app.races[i].laps:
                print(i, 'hi wassup')
                swimmer.finished = True
                swimmer.step(app.paused, app.selectedStroke, app.races[i], app.timer, app.margin*1.5)
                i+=1 
                continue
            if app.races[i].lap != app.races[i].laps:
                if app.races[i].lap % 2 == 0 and app.selectedCourse == 'SCM':
                    app.races[i].fifty += 1
                elif app.selectedCourse == 'LCM':
                    app.races[i].fifty += 1
                app.races[i].lap += 1
        elif (app.swimmers[leadSwimmer].x < app.screenRight - app.margin and app.direction == 1 or
            app.screenLeft + 3*app.margin + app.pool.length - app.width < app.swimmers[leadSwimmer].x and app.direction == -1): 
            swimmer.x += swimmerSpeeds[app.races[i].fifty-1]*-swimmer.dir*app.playbackSpeed
        elif (app.swimmers[leadSwimmer].x >= app.screenRight - app.margin and app.direction == 1 or
            app.screenLeft + 3*app.margin + app.pool.length - app.width >= app.swimmers[leadSwimmer].x and app.direction == -1): 
            if i == leadSwimmer:
                app.screenLeft -= leadSwimmerSpeeds[app.races[i].lap-1]*app.direction*app.playbackSpeed
            elif app.races[i].lap == app.races[leadSwimmer].lap:
                swimmer.x -= (leadSwimmerSpeeds[app.races[i].fifty-1] - swimmerSpeeds[app.races[i].fifty-1])*-swimmer.dir*app.playbackSpeed
            else:
                swimmer.x += (leadSwimmerSpeeds[app.races[i].fifty-1] + swimmerSpeeds[app.races[i].fifty-1])*-swimmer.dir*app.playbackSpeed
        elif ((app.races[i].lap != app.races[leadSwimmer].lap) and 
            app.swimmers[leadSwimmer].x <= app.screenRight - app.margin and app.direction == swimmer.dir or
            app.screenLeft + 3*app.margin + app.pool.length - app.width <= app.swimmers[leadSwimmer].x and app.direction == swimmer.dir): 
            swimmer.x += (swimmerSpeeds[app.races[i].fifty-1])*-swimmer.dir*app.playbackSpeed
        i+=1

def getButtons(app): #homescreen buttons
    return [(app.width*0.9, app.height*0.1, '?', None),
            (app.width*0.4, app.height*0.35, 1, 'mode'),
            (app.width*0.6, app.height*0.35, 2, 'mode'),
            (app.width*0.35, app.height*0.55, 'LCM', 'course'),
            (app.width*0.65, app.height*0.55, 'SCM', 'course'),
            (app.width*0.3, app.height*0.65, 50, 'distance'),
            (app.width*0.5, app.height*0.65, 100, 'distance'),
            (app.width*0.7, app.height*0.65, 200, 'distance'),
            (app.width*0.2, app.height*0.75, 'FR', 'stroke'),
            (app.width*0.35, app.height*0.75, 'BK', 'stroke'),
            (app.width*0.5, app.height*0.75, 'BR', 'stroke'),
            (app.width*0.65, app.height*0.75, 'FL', 'stroke'),
            (app.width*0.8, app.height*0.75, 'IM', 'stroke')
            ]

def getStrategyButtons(app):
    return [(app.width/4, app.height*0.3, 'Go out aggressive'),
            (app.width/4, app.height*0.45, 'Hold pace better'),
            (app.width/4, app.height*0.6, 'Similar to past splits')]

def getBestWorstStrokeButtons(app):
    return [(app.width*0.25, app.height*0.4, 'FL'),
            (app.width*0.75, app.height*0.4, 'BK'),
            (app.width*0.25, app.height*0.7, 'BR'),
            (app.width*0.75, app.height*0.7, 'FR')
             ]

def getValidRaces(app):
    return [(50, 'FR'), (100, 'FR'), (200, 'FR'),
            (100, 'BK'), (200, 'BK'),
            (100, 'BR'), (200, 'BR'),
            (100, 'FL'), (200, 'FL'),
            (200, 'IM')]

def resetApp(app):
    app.width, app.height = 800, 800
    app.homescreen = True
    app.instructions = False
    app.instructionsText = instructions.Instructions(app.width)
    app.getNumSwimmers = False
    app.numSwimmers = ''
    app.createSwimmers = False
    app.prepRace = False
    app.prepMode2 = False
    app.selectedMode = None
    app.selectedCourse = None
    app.selectedDistance = None
    app.selectedStroke = None
    app.buttonR = app.width*0.04
    app.paused = True
    app.racing = False
    app.direction = 1 #swimming right
    app.screenLeft = 0
    app.screenRight = app.screenLeft + app.width
    app.margin = app.width / 10 #margin to left of pool
    app.swimmerLane = 0
    app.diving = True
    app.playbackSpeed = 4
    app.timer = 0
    app.buttons = getButtons(app)
    app.strategyButtons = getStrategyButtons(app)
    app.validRaces = getValidRaces(app)
    app.bestWorstStrokes = getBestWorstStrokeButtons(app)
    app.invalidRace = False
    app.raceFinished = False
    app.swimmers = []
    app.races = []
    app.currSwimmer = 0 #the current swimmer getting info for
    app.currSwimmerName = ''

    
def main():
    runApp()

main()
