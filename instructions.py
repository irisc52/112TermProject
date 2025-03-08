from cmu_graphics import *

class Instructions:
    def __init__(self, dimension):
        self.font = 'monospace'
        self.l = dimension #length = width
        self.text = ['About the Swimulator',
                     '                       ',
                     "If you are a swimmer, you know how important visualization is before races.",
                     "If not, just trust me. It is very important.",
                     '                                    ',
                     "In mode 1, you will enter exact splits for your race. This would be helpful if you recently swam a race",
                     "and forgot to video it :( or if you have very (very) specific goals for a race.",
                     '                               ',
                     "There are three options for mode 2.",
                     "1. Having trouble starting fast enough in your races? This mode is for you. Enter a goal time,",
                     "and the Swimulator will provide splits needed to go out aggressive ",
                     "2. Are you going out too fast? Want to hold pace better? Enter a goal time and the Swimulator will",
                     "generate splits that are close in time to each other.",
                     "3. Maybe you are satisfied with your splits. Enter exact splits from three races with similar times to", 
                     "your goal time, and the Swimulator will generate a race that averages these splits.",
                     '                                 ',
                     "Choose any valid race and course and watch your race come to life. ",
                     '                                 ',
                     "You can also have fun with this! Become Michael Phelps or Katie Ledecky from your own computer. In fact,",
                     "break world records! Go a 30 second 100 free!! The world (the pool) is your oyster! ",
                     '                         ',
                     "Press b to return to the homescreen. Have fun!",
                     '                               ',
                     "inspired by the New York Times 3D animations for the 2024 Olympics"]
 
    
    def write(self):
        for i in range(len(self.text)):
            if i+1 == len(self.text): #last line
                italic = True
            else:
                italic = False
            if i+3 == len(self.text) or i == 0: #return to homescreen
                bold=True
            else:
                bold=False
            drawLabel(self.text[i], self.l*0.05, self.l*(0.1 + 0.03*i), italic=italic, 
                      align='left', bold=bold, font='monospace')
    
    