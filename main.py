import pygame
import sys
import matplotlib.image as mpimg
from pygame.locals import *
"""
Game project 
"""

height = 600
width = 1200
dictControls = {K_w : "movingUp", K_s : "movingDown", K_a : "movingLeft", K_d : "movingRight"}
clock=pygame.time.Clock()
fps = 60



pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill([0, 0, 255])



def load_image(path):
    return pygame.image.load(path)

def terminate():
    pygame.quit()
    sys.exit()

class Score():
    val = 0
    font = pygame.font.SysFont("ocraextended", 50)

    def __init__(self):
        self.text = self.font.render(str(self.val), True, [0, 0, 0])
        self.textRect = self.text.get_rect()
        self.textRect.center = (round(width/2), height - 50)

    def update(self):
        self.val = self.val + 5/fps # TODO : Slow down points maybe ?
        self.text = (self.font).render(str(round(self.val)), True, [0, 0, 0])

class Submarine():

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("assets/submarineTransparent.png").convert_alpha()
        self.boundaries = mpimg.imread("assets/submarineTransparentBoundaries.png").T
        self.imageRect = self.image.get_rect()
        self.imageRect.center = self.pos # TODO : set center of the image at the center of the screen instead of topleft of image


    def isFreeSpace(self,pos):

        posInSub = self.globPos2SubPos(pos)
        if posInSub[0]<=0 or posInSub[1]<=0:
            return False
        elif posInSub[0] > len(self.boundaries[0]) or posInSub[1] > len(self.boundaries[0][0]):
            return False
        elif self.boundaries[0][posInSub[0]][posInSub[1]] == 1:
            return True
        else:
            return False

    def globPos2SubPos(self,pos):

        posInSub = [pos[0]-self.imageRect[0],pos[1]-self.imageRect[1]]
        return posInSub



class Pilot():
    dictControls = {K_w : "movingUp", K_s : "movingDown", K_a : "movingLeft", K_d : "movingRight"}
    vel = 10
    state = [] # empty is still

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("assets/perso.png").convert_alpha()
        heightImg = self.image.get_size()[1]
        widthImg = self.image.get_size()[0]
        self.image = pygame.transform.scale(self.image, (round(widthImg/3), round(heightImg/3))) # TODO : normalize according to screen size
        self.imageRect=self.image.get_rect()
        self.imageRect.center = self.pos

    def update(self,key):
        if key == K_w: # up
            self.pos[1] = self.pos[1] - self.vel
            self.imagerect.topleft = self.pos

        if key == K_s: # down
            self.pos[1] = self.pos[1] + self.vel
            self.imagerect.topleft = self.pos

        if key == K_a: # left
            self.pos[0] = self.pos[0] - self.vel
            self.imagerect.topleft = self.pos

        if key == K_d: # right
            self.pos[0] = self.pos[0] + self.vel
            self.imagerect.topleft = self.pos


    def updateState(self,submarine):


        newPos = self.pos.copy()
        if len(self.state) == 0:
            return
        print(self.pos)
        if "movingUp" in self.state: # up
            newPos[1] = self.pos[1] - self.vel


        if "movingDown" in self.state: # down
            newPos[1] = self.pos[1] + self.vel


        if "movingLeft" in self.state: # left
            newPos[0] = self.pos[0] - self.vel


        if "movingRight" in self.state: # right
            newPos[0] = self.pos[0] + self.vel

        print(self.pos)
        print("----")
        if submarine.isFreeSpace(newPos):
            self.pos = newPos

            self.imageRect.center = newPos








pilot = Pilot()
submarine = Submarine()
score = Score()

if __name__ == '__main__':



    # main loop
    running = True
    while running:


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in pilot.dictControls.keys():
                    pilot.state.append(pilot.dictControls[event.key])
                    # pilot.update(event.key)


                if event.key == K_ESCAPE:
                    running = False
                    terminate()

            if event.type == KEYUP:
                if event.key in pilot.dictControls.keys():
                    pilot.state.remove(dictControls[event.key])







            if event.type == pygame.QUIT:
                running = False
                terminate()



        pilot.updateState(submarine)
        score.update()


        screen.fill([0, 0, 255])
        screen.blit(submarine.image, submarine.imageRect)
        screen.blit(pilot.image, pilot.imageRect)
        screen.blit(score.text, score.textRect)

        pygame.display.update()
        clock.tick(fps)
