import pygame
import sys
from pygame.locals import *
"""
Game project 
"""

height = 600
width = 1200

clock=pygame.time.Clock()
fps = 25

pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill([0, 0, 255])
pygame.display.flip()

def load_image(path):
    return pygame.image.load(path)

def terminate():
    pygame.quit()
    sys.exit()

class submarine():
    pass


class pilot():
    allowedKeys = [K_w,K_a,K_s,K_d]
    vel = 10

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("perso.png").convert_alpha()
        heightImg = self.image.get_size()[1]
        widthImg = self.image.get_size()[0]
        self.image = pygame.transform.scale(self.image, (round(widthImg/2), round(heightImg/2))) # TODO : normalize according to screen size
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





if __name__ == '__main__':
    pilot = pilot()

    running = True
    while running:


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in pilot.allowedKeys:
                    pilot.update(event.key)

                if event.key == K_ESCAPE:
                    running = False
                    terminate()







            if event.type == pygame.QUIT:
                running = False
                terminate()



        screen.fill([0, 0, 255])
        screen.blit(pilot.image, pilot.imagerect)

        pygame.display.update()
        clock.tick(fps)
