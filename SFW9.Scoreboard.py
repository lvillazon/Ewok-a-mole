import sys, pygame, os, json
from enum import Enum

#############################################

class state(Enum):
    leaderboard = 1
    select_track = 2
    playing = 3
    totting_up = 4
    quit_prog = 6

class HighScoreTable():
    # maintains an always-sorted list of the best scores and players
    def __init__(self):
        self.all_scores = []
        if os.path.isfile('hi-scores.json'):
            with open('hi-scores.json') as f:
                self.all_scores = json.load(f)
                print(self.all_scores)

    def AddScore(self, score, name):
        #adds a new hi-score at the correct position
        self.all_scores.insert(self.GetRanking(score), (score, name))
        with open('hi-scores.json', 'w') as f: #save hi-score table
            json.dump(self.all_scores, f)

    def GetRanking(self, score):
        # return the position in the hi-score table that this score would be, but doesn't actually add it.
        # In the case of duplicate scores, the more recent score is placed higher
        i = 0
        while (i<len(self.all_scores)) and (score < self.all_scores[i][0]):
            #keep going 'till we get to the end or find an existing score we have beaten (or equalled)
            i = i
        print("rank=",i)
        return i

    def GetRankingText(self, score):
        # returns the rank as an ordinal string: 1st, 2nd, 3rd etc
        ordinal_text = {0:'th', 1:'st', 2:'nd', 3:'rd', 4:'th', 5:'th', 6:'th', 7:'th', 8:'th', 9:'th'}
        rank = self.GetRanking(score) +1 #because we don't want to talk of 0th rank, even though the list is 0-indexed
        print(self.all_scores)
        return str(rank)+ordinal_text[rank]

this crashes when adding an item with score 3. Should insert at the front of the list.
    

def ShowTitle(text, colour_name):
    screen.fill((0,0,0))
    colour = (255,0,0) #red is the default colour
    if colour_name == "green":
        colour = (0,128,0)
    if colour_name == "yellow":
        colour = (255,255,0)
    titleText = titleFont.render(text, True, colour)
    screen.blit(titleText, (screen_width//2 - titleText.get_width()//2, screen_height//2 - titleText.get_height()//2))
    pygame.display.flip()
    pygame.event.clear()


def RunSelectTrack():
    #draw the static graphic elements
    ShowTitle("SELECT TRACK...", "yellow")

    screen.fill((0,0,0))
    colour = (0,128,0) #green
    track_list = {
                    1:("Love Pledge/The Arena",           171.0),
                    2:("Grievous Speaks to Lord Sidious", 359.0),
                    3:("The Imperial March", 1106.5),
                    4:("Kylo Ren Arrives at the Battle", 1207.0),
                    5:("The Imperial Suite", 1250.0),
                    6:("Hope", 1506.0)
                    }

    menuX = 200
    menuY = 200
    for track in track_list:
        menu_number = menuFont.render(str(track) + ". ", True, colour)
        menu_item = menuFont.render(track_list[track][0], True, colour)
        screen.blit(menu_number, (menuX-menu_number.get_width(), menuY))
        screen.blit(menu_item, (menuX+20, menuY))
        menuY = menuY + menu_item.get_height()*1.5
    pygame.display.flip()
    pygame.event.clear()
   
    track_number = -1
    while track_number == -1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return state.leaderboard
                if event.key == pygame.K_1:
                    track_number = 1
                if event.key == pygame.K_2:
                    track_number = 2
                if event.key == pygame.K_3:
                    track_number = 3
                if event.key == pygame.K_4:
                    track_number = 4
                if event.key == pygame.K_5:
                    track_number = 5
                if event.key == pygame.K_6:
                    track_number = 6
                if event.key == pygame.K_7:
                    track_number = 7
                if event.key == pygame.K_8:
                    track_number = 8
                if event.key == pygame.K_9:
                    track_number = 9
                if event.key == pygame.K_0:
                    track_number = 0

    pygame.mixer.music.play(-1,track_list[track_number][1])
    return state.playing

def RunPlaying():
    #draw the static graphic elements
    ShowTitle("EWOK 'EM ALL!!", "red")
    
    #eventually this will run for 1 minute unless a key is pressed to terminate early (or pause?)
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return state.select_track
                if event.key == event.key == pygame.K_SPACE:
                    if paused == False:
                        pygame.mixer.music.pause()
                        paused = True
                    else:
                        pygame.mixer.music.unpause()
                        paused = False
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(2000) #fade out over 2 seconds
                    return state.totting_up


class ScoreBox:
    def __init__(self, position):
        self.position = position
        self.width = screen_width/20
        self.height = screen_height/10
        self.x = screen_width/2 + (self.width+self.width/3)*(self.position-4)
        self.y = screen_height/2 - self.height*2
        self.line_width = 4
        self.score = 0
        self.selected = False
        self.Draw()

    def Draw(self):
        if self.selected == True:
            col = pygame.Color('green')
        else:
            col = pygame.Color('dark green')

        pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(self.x,self.y,self.width,self.height),0) #blank the box
        pygame.draw.rect(screen, col, pygame.Rect(self.x,self.y,self.width,self.height),self.line_width)
        score_text = titleFont.render(str(self.score), True, pygame.Color('dark green'))
        x = self.x+self.width/2 - score_text.get_width()//2
        y = self.y+self.height/2 - score_text.get_height()//2
        screen.blit(score_text, (x, y))
        pygame.display.flip()
        pygame.display.update()

    def SetSelected(self, s):
        if not s==self.selected:
            self.selected = s
            self.Draw()

    def SetScore(self, s):
        if not s==self.score:
            self.score = s
            self.Draw() #redraw the box to blank the previous contents


def RunTottingUp():
    #draw the static graphic elements
    screen.fill((0,0,0))
    ShowTitle("TOTAL SCORE", "green")

    boxes = []            
    for i in range(0,8):
        new_box = ScoreBox(i)
        boxes.append(new_box)

    cursor_pos = 0
    boxes[cursor_pos].SetSelected(True)
    total = 0 #final score for the most recent game

    number_keys = {
        pygame.K_0:0,
        pygame.K_1:1,
        pygame.K_2:2,
        pygame.K_3:3,
        pygame.K_4:4,
        pygame.K_5:5,
        pygame.K_6:6,
        pygame.K_7:7,
        pygame.K_8:8,
        pygame.K_9:9}
    
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    EnterName(total)
                    return state.leaderboard
                
                if event.key == pygame.K_RIGHT:
                    cursor_pos = cursor_pos + 1
                    if cursor_pos > 7:
                        cursor_pos = 7
                if event.key == pygame.K_LEFT:
                    cursor_pos = cursor_pos - 1
                    if cursor_pos < 0:
                        cursor_pos = 0
                if event.key in number_keys:
                    boxes[cursor_pos].SetScore(number_keys[event.key])

                total = 0    
                for i in range(0,8):
                    boxes[i].SetSelected(False) #unselect all boxes
                    total = total + boxes[i].score
                boxes[cursor_pos].SetSelected(True) #now selected the new one
                # display the total score
                total_text = titleFont.render(str(total), True, pygame.Color('green'))
                x = screen_width//2 - total_text.get_width()//2
                y = screen_height//2 + total_text.get_height()
                pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(0,y,screen_width,boxes[0].height),0) #blank the box
                screen.blit(total_text, (x, y))
                pygame.display.flip()
                if cursor_pos < 7:
                    cursor_pos = cursor_pos+1
                
    
def RunLeaderboard():
    #draw the static graphic elements
    screen.fill((0,0,0))
    ShowTitle("TODAY's HI-SCORES", 'yellow')
    
    pygame.event.clear()
    #eventually this will display the current hi-scores
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return state.quit_prog
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return state.select_track

def EnterName(score):
    #draw the static graphic elements
    screen.fill((0,0,0))
    ShowTitle("You rank "+hi_scores.GetRankingText(score), "green")
    
    pygame.event.clear()
    name = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    hi_scores.AddScore(score, name)
                    return state.leaderboard
                else:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name = name + event.unicode
                    name_text = hi_scoreFont.render(name, True, pygame.Color('yellow'))
                    x = screen_width//2 - name_text.get_width()//2
                    y = screen_height//2 + name_text.get_height()
                    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(0,y,screen_width,name_text.get_height()),0) #blank the box
                    screen.blit(name_text, (x, y))
                    pygame.display.flip()

###############################################
# initialisation stuff

pygame.init()
screen_width = 1280
screen_height = 1024
screen = pygame.display.set_mode((screen_width,screen_height))

# needs "amixer cset numid=3 2" at command line to send audio to HDMI
pygame.mixer.music.load('sounds/star_wars.ogg')

#fonts
titleFont = pygame.font.Font('fonts/droid/IDroid.otf', 60)
menuFont = pygame.font.Font('fonts/neuropol.ttf', 30)
hi_scoreFont = pygame.font.Font('fonts/neuropol.ttf', 60)

#load hi-score table
hi_scores = HighScoreTable()

currentState = state.leaderboard
       
#############################################
#main loop controls the finite state machine
while currentState != state.quit_prog:
    pygame.event.pump()
    if currentState == state.select_track:
        currentState = RunSelectTrack()
    if currentState == state.playing:
        currentState = RunPlaying()
    if currentState == state.totting_up:
        currentState = RunTottingUp()
    if currentState == state.leaderboard:
        currentState = RunLeaderboard()

pygame.quit()
sys.exit()


