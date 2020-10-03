import pygame
import sys
import matplotlib.image as mpimg
import numpy
from pygame.locals import *
from utils.layouts import *
import time

height = 600
width = 1200
dictControls = {K_w : "movingUp", K_s : "movingDown", K_a : "movingLeft", K_d : "movingRight"}
clock=pygame.time.Clock()
fps = 60
subHeight = 333
subWidth = 750
layout = 0


pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill([0, 0, 255])

repairing = "repairing"

def getDamage(submarine):
    nComp = len(submarine.compartments)
    proba = 0
    nrand = numpy.random.rand()*100
    if nrand>proba:
        return int(numpy.floor(numpy.random.rand()*nComp))
    else:
        return None



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

    def update(self, gameOver = False):
        self.val = self.val + 5/fps
        self.text = (self.font).render(str(round(self.val)), True, [0, 0, 0])
        if gameOver:
            self.text = self.font.render("GAME OVER", True, [0, 0, 0])



class Submarine():

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("assets/submarineLayout" + str(layout) + "Transparent.png").convert_alpha()
        self.boundaries = mpimg.imread("assets/submarineLayout" + str(layout) + "TransparentBoundaries.png").T
        self._createBackground("assets/backgroundSub.png", "assets/submarineLayout" + str(layout) + "Transparent.png")
        # self.image.paste(self.image, (0,0) , self.backgroundImage)
        self.imageRect = self.image.get_rect()
        self.imageRect.center = self.pos # TODO : set center of the image at the center of the screen instead of topleft of image
        self._populateCompartments(layout)

    def _createBackground(self, backgroundPath, layoutPath):
        imgBackground = mpimg.imread(backgroundPath)
        imgLayout = mpimg.imread(layoutPath)
        if numpy.size(imgLayout) != numpy.size(imgBackground):
            raise Exception("Submarine background and submarine image don't have the same size")
        for i in range(len(imgLayout)):
            for j in range(len(imgLayout[0])):
                if imgLayout[i][j][3] != 0:
                    imgBackground[i][j] = imgLayout[i][j]
        mpimg.imsave("assets/tempBackground.png", imgBackground)
        self.backgroundImage = load_image("assets/tempBackground.png")



    def _populateCompartments(self, layout):
        compartmentsInfo = LAYOUTS[layout][0]
        self.compartments = []
        id = 0
        for compInfo in compartmentsInfo:
            compartment = Compartment(compInfo, id)
            self.compartments.append(compartment)
            id += 1

    def getCompartmentId(self, pos):
        posSubRef = self.globPos2SubPos(pos)
        for comp in self.compartments:
            if comp.isInside(posSubRef):
                return comp.id

    def isFreeSpace(self, pos):
        """

        :param pos: global position of the pilot
        :return: 1 if in the submarine and on a free cell 0 else
        """
        posInSub = self.globPos2SubPos(pos)
        return self.boundaries[0][posInSub[0]][posInSub[1]]
        # if posInSub[0]<=0 or posInSub[1]<=0:
        #    return False
        # elif posInSub[0] > len(self.boundaries[0]) or posInSub[1] > len(self.boundaries[0][0]):
        #    return False
        # elif self.boundaries[0][posInSub[0]][posInSub[1]] == 1:
        #    return True
        # else:
        #    return False

    def globPos2SubPos(self,pos):

        posInSub = [pos[0]-self.imageRect[0], pos[1]-self.imageRect[1]]
        return posInSub

    def updateCompartments(self, pilot):
        pilotCompId = self.getCompartmentId(pilot.pos)
        for comp in self.compartments:
            if comp.health < 100 and pilotCompId == comp.id and repairing in pilot.state:
                comp.health = min(comp.health + 20, 100)
            elif comp.isDamaged:
                comp.health = max(comp.health - 10, 0)

            if comp.health >= 100 and comp.isDamaged:
                comp.health = 100
                comp.isDamaged = False

            if comp.health <= 0:
                return True

class Compartment():

    isDamaged = False
    health = 100

    def __init__(self, compartmentInfo, id):
        self.id = id
        self.topRight = compartmentInfo[0]
        self.bottomLeft = compartmentInfo[1]
        self.functions = compartmentInfo[2]

    def isInside(self, pos):
        "returns true if pos is inside the compartment"
        return pos[0] >= self.topRight[0] and pos[1] >= self.topRight[1] and pos[0] < self.bottomLeft[0] and pos[1] < self.bottomLeft[1]

class Pilot():
    dictControls = {K_w : "movingUp", K_s : "movingDown", K_a : "movingLeft", K_d : "movingRight", K_e: repairing}
    vel = 10
    state = [] # empty is still

    def __init__(self):
        self.pos = [round(width/2), round(height/2)]
        self.image = load_image("assets/wn.webp").convert_alpha()
        heightImg = self.image.get_size()[1]
        widthImg = self.image.get_size()[0]
        self.image = pygame.transform.scale(self.image, (round(widthImg/3), round(heightImg/3))) # TODO : normalize according to screen size
        self.imageRect=self.image.get_rect()
        self.imageRect.center = self.pos

    def update(self, key): # Obsolete

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

        if "movingUp" in self.state: # up
            newPos[1] = self.pos[1] - self.vel


        if "movingDown" in self.state: # down
            newPos[1] = self.pos[1] + self.vel


        if "movingLeft" in self.state: # left
            newPos[0] = self.pos[0] - self.vel


        if "movingRight" in self.state: # right
            newPos[0] = self.pos[0] + self.vel


        if submarine.isFreeSpace(newPos):
            self.pos = newPos

            self.imageRect.center = newPos






pilot = Pilot()
submarine = Submarine()
screen.blit(submarine.backgroundImage, submarine.imageRect)
score = Score()
nextVal = 5
frameCounter = 0

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
                    pilot.state.remove(pilot.dictControls[event.key])







            if event.type == pygame.QUIT:
                running = False
                terminate()


        pilot.updateState(submarine)
        score.update()
        if score.val > nextVal:
            compartmentDamaged = getDamage(submarine)
            nextVal = score.val + numpy.random.rand()*25
            if compartmentDamaged is not None:
                submarine.compartments[compartmentDamaged].isDamaged = True

        if frameCounter > 30:
            gameOver = submarine.updateCompartments(pilot)
            frameCounter = 0
            if gameOver:
                score.update(gameOver=True)
                running = False
                pygame.time.delay(5000)

        screen.fill([0, 0, 255])
        # screen.blit(submarine.backgroundImage, submarine.imageRect)
        #screen.blit(background, position, position)
        screen.blit(submarine.image, submarine.imageRect)
        for comp in submarine.compartments:
            if comp.isDamaged:
                # pygame.draw.rect(submarine.image, [0, 255, 0], ((comp.bottomLeft[0] - comp.topRight[0])/2, comp.topRight[1] + 15, 60, 5))
                pygame.draw.rect(screen, [255, 0, 0],
                                 (int(submarine.imageRect[0] + comp.topRight[0] + (comp.bottomLeft[0] - comp.topRight[0])/4),submarine.imageRect[1] + comp.topRight[1] + 15, 60, 10))
                pygame.draw.rect(screen, [0, 255, 0],
                (int(submarine.imageRect[0] + comp.topRight[0] + (comp.bottomLeft[0] - comp.topRight[0]) / 4),submarine.imageRect[1] + comp.topRight[1] + 15, int(comp.health*60/100), 10))
        screen.blit(pilot.image, pilot.imageRect)
        screen.blit(score.text, score.textRect)
        pygame.display.update()
        frameCounter += 1
        clock.tick(fps)
