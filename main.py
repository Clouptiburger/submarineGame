import pygame
import sys
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
pygame.display.flip()

def load_image(path):
    return pygame.image.load(path)

def terminate():
    pygame.quit()
    sys.exit()

class Submarine():


    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("submarineTransparent.png").convert_alpha()
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = self.pos # TODO : set center of the image at the center of the screen instead of topleft of image



class Pilot():
    dictControls = {K_w : "movingUp", K_s : "movingDown", K_a : "movingLeft", K_d : "movingRight"}
    vel = 10
    state = [] # empty is still

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("perso.png").convert_alpha()
        heightImg = self.image.get_size()[1]
        widthImg = self.image.get_size()[0]
        self.image = pygame.transform.scale(self.image, (round(widthImg/3), round(heightImg/3))) # TODO : normalize according to screen size
        self.imagerect=self.image.get_rect()
        self.imagerect.topleft = self.pos # TODO : set center of the image at the center of the screen instead of topleft of image

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


    def updateState(self):
        if len(self.state) == 0:
            return
        newState = self.state[-1]
        if newState == "movingUp": # up
            self.pos[1] = self.pos[1] - self.vel
            self.imagerect.topleft = self.pos

        if newState == "movingDown": # down
            self.pos[1] = self.pos[1] + self.vel
            self.imagerect.topleft = self.pos

        if newState == "movingLeft": # left
            self.pos[0] = self.pos[0] - self.vel
            self.imagerect.topleft = self.pos

        if newState == "movingRight": # right
            self.pos[0] = self.pos[0] + self.vel
            self.imagerect.topleft = self.pos





if __name__ == '__main__':
    pilot = Pilot()
    submarine = Submarine()
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


        if pilot.state != []:
            print(pilot.state)


        pilot.updateState()
        screen.fill([0, 0, 255])
        screen.blit(submarine.image, submarine.imagerect)
        screen.blit(pilot.image, pilot.imagerect)

        pygame.display.update()
        clock.tick(fps)
