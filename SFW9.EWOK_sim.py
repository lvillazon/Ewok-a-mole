import sys, pygame, os
from enum import Enum
# simulate the sequence of EWOK-A-MOLE targets, to figure out choreography

pygame.init()

class state(Enum):
    idle = 1
    can_score = 2
    non_scoring = 3
    hit = 4
    miss = 5

choreography = []

class Target():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.state = state.idle
        self.SIZE = 10
        self.end_timer = 0

    def SetState(self, state):
        if state == state.can_score:
            self.end_timer = pygame.time.get_ticks() + 2000
        if state == state.non_scoring:
            self.end_timer = pygame.time.get_ticks() + 3000
        self.state = state

    def Update(self):
        if pygame.time.get_ticks() > self.end_timer:
            if self.state == state.can_score:
                self.SetState(state.non_scoring)
            elif self.state == state.non_scoring:
                self.SetState(state.miss)

    def Draw(self):
#        print("drawing", self.id)
        if self.state == state.idle:
            pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.SIZE, 0)
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y), self.SIZE, 2)
        if self.state == state.can_score:
            pygame.draw.circle(screen, (0,255,0), (self.x, self.y), self.SIZE, 0)
        if self.state == state.non_scoring:
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y), self.SIZE, 0)
        if self.state == state.hit:
            pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.SIZE*2, 0)
        if self.state == state.miss:
            pygame.draw.circle(screen, (100,100,100), (self.x, self.y), self.SIZE, 0)
        pygame.display.update()


width = 1464 #same aspect ratio as actual game board
height = 732
screen = pygame.display.set_mode((width,height))


#############################################

targets = [
    Target(1, 100,150),
    Target(2, 350,550),
    Target(3, 450,200),
    Target(4, 700,650),
    Target(5, 800,300),
    Target(6, 900,380),
    Target(7, 1100,70),
    Target(8, 1364,632)]

countdown_font = pygame.font.Font(None, 30)
countdown_rect = pygame.Rect(0,0, 100,50)

quit = False
replay = False
game_start = pygame.time.get_ticks()
while not quit and not replay:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_p:
                print(choreography)
            if event.key == pygame.K_r:
                replay = True
            if event.key == pygame.K_1:
                choreography.append([0, pygame.time.get_ticks()-game_start])
                targets[0].SetState(state.can_score)
            if event.key == pygame.K_2:
                choreography.append([1, pygame.time.get_ticks()-game_start])
                targets[1].SetState(state.can_score)
            if event.key == pygame.K_3:
                choreography.append([2, pygame.time.get_ticks()-game_start])
                targets[2].SetState(state.can_score)
            if event.key == pygame.K_4:
                choreography.append([3, pygame.time.get_ticks()-game_start])
                targets[3].SetState(state.can_score)
            if event.key == pygame.K_5:
                choreography.append([4, pygame.time.get_ticks()-game_start])
                targets[4].SetState(state.can_score)
            if event.key == pygame.K_6:
                choreography.append([5, pygame.time.get_ticks()-game_start])
                targets[5].SetState(state.can_score)
            if event.key == pygame.K_7:
                choreography.append([6, pygame.time.get_ticks()-game_start])
                targets[6].SetState(state.can_score)
            if event.key == pygame.K_8:
                choreography.append([7, pygame.time.get_ticks()-game_start])
                targets[7].SetState(state.can_score)

    countdown_text = countdown_font.render(str(int((60-(pygame.time.get_ticks()-game_start)/1000))), True, (255,0,0))
    screen.fill((0,0,0), countdown_rect)
    screen.blit(countdown_text,(0,0))
    pygame.display.flip()
    pygame.event.clear()
    for i in targets:
        i.Draw()
        i.Update()

# reset all the targets before any replay
for i in targets:
    i.SetState(state.idle)
    i.Draw()
pygame.event.pump()

step_counter = 0
replay_start = pygame.time.get_ticks()
while replay and not quit: # replay the saved choreography
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_d:
                print(choreography)
                quit = True

    if pygame.time.get_ticks() > replay_start + choreography[step_counter][1]:
        targets[choreography[step_counter][0]].SetState(state.can_score)
        step_counter = step_counter +1
        if step_counter == len(choreography):
            step_counter = 0
            replay_start = pygame.time.get_ticks()
    for i in targets:
        i.Draw()
        i.Update()

print(choreography)

pygame.quit()
sys.exit()

#    pygame.event.clear()
#    pygame.time.delay(1000)
