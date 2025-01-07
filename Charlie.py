import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Charlie's Farm")
clock = pygame.time.Clock()
powerfont = pygame.font.Font(None, 50)
center = (600, 450)
transparent = (0, 0, 0, 0)

#ADD POWER AND TIME DISPLAY
#AND WIN/LOSE SCREENS


#i made a dictionary for cooldown function
cooldowns = {}

def cooldown(key, duration): 
    current_time = time.time()
    if key not in cooldowns or current_time - cooldowns[key] >= duration:
        cooldowns[key] = current_time
        return True
    return False

    
# Image Import Function

def imgimport(img, size):
    newmap = pygame.image.load(img).convert_alpha()
    newmap = pygame.transform.scale(newmap,(size))
    return newmap

# VHS effect
VHS = []
for i in range(6):
    VHS.append(pygame.image.load(f"Data/States/Mainscreen/VHS/{i}.png"))

VHSINDEX = 0

def vhs(screen):
    global VHSINDEX
    screen.blit(VHS[VHSINDEX], (0, 0))
    VHSINDEX += 1
    if VHSINDEX >= len(VHS):
        VHSINDEX = 0

#Rain effect
CHS = []
for i in range(7):
    CHS.append(f"Data/States/Map/Rain/{i}.png")
    CHS[i] = imgimport(CHS[i], (1920, 1080))

CHSINDEX = 0

def rain(screen):
    global CHSINDEX
    screen.blit(CHS[CHSINDEX], (0, 0))
    CHSINDEX += 1
    if CHSINDEX >= len(CHS):
        CHSINDEX = 0
#==================================================================================================#

#Mainscreen Buttons
playbutton = pygame.image.load("Data/States/Mainscreen/Playbutton.png")
playbuttonp = pygame.image.load("Data/States/Mainscreen/PlaybuttonP.png")
playbuttonrect = playbutton.get_rect(center = (300,600))
title = powerfont.render("Charlie's Farm", True, "White")

quitbutton = pygame.image.load("Data/States/Mainscreen/Quitbutton.png")
quitbuttonp = pygame.image.load("Data/States/Mainscreen/QuitbuttonP.png")
quitbuttonrect = quitbutton.get_rect(center = (300, 900))

optionsbutton = pygame.image.load("Data/States/Mainscreen/Optionsbutton.png")
optionsbuttonp = pygame.image.load("Data/States/Mainscreen/OptionsbuttonP.png")
optionsbuttonrect = optionsbutton.get_rect(center = (375, 750))

charliepfp = pygame.image.load("Data/States/Mainscreen/Charlie.png")
#==================================================================================================#

# Customscreen Buttons
customborders = pygame.image.load("data/states/custom/CustomBorders.png")
customborders = pygame.transform.scale(customborders,(1200,900))

backbutton = pygame.image.load("data/states/custom/Backbutton.png")
backbuttonp = pygame.image.load("data/states/custom/BackbuttonP.png")
backbuttonrect = backbutton.get_rect(center = (200, 850))

arrowr = pygame.image.load("data/states/custom/ArrowR.png")
arrowr = pygame.transform.scale(arrowr, (30, 30))
arrowl = pygame.image.load("data/states/custom/ArrowL.png")
arrowl = pygame.transform.scale(arrowl, (30, 30))

beginbutton = pygame.image.load("data/states/custom/Begin.png")
beginbuttonr = pygame.image.load("data/states/custom/BeginR.png")
beginbuttonp = pygame.image.load("data/states/custom/BeginP.png")
beginbuttonrect = beginbutton.get_rect(center = (1500, 850))
#==================================================================================================#

# Character Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, diffculty):
        super().__init__()
        self.name = name
        self.diffculty = diffculty
        self.pos = 3
        self.image = None

    def iskilled(self):
        pass

    def killplayer(self):
        pass

    def move(self):
        pass

    def display(self):
        global camerapos, incameras
        if camerapos == self.pos and incameras:
            screen.blit(self.image, (400, 400))

    def update(self):
        self.display()



class CustomEnemy(pygame.sprite.Sprite):
    def __init__(self, name, difficulty, pfp, pfpx, pfpy):
        super().__init__()
        self.name = name
        self.difficulty = difficulty
        self.image = pfp
        self.image = pygame.transform.scale(self.image, (180, 160))
        self.pfpx = pfpx
        self.pfpy = pfpy
        self.rect = self.image.get_rect(center = (self.pfpx, self.pfpy))
        self.rectleft = arrowl.get_rect(center = (self.pfpx - 75, self.pfpy + 125))
        self.rectright = arrowr.get_rect(center = (self.pfpx + 75, self.pfpy + 125))

    def arrowdisplay(self):
        screen.blit(arrowl, self.rectleft)
        screen.blit(arrowr, self.rectright)
        difficultydisplay = powerfont.render(str(self.difficulty), True, "White")
        screen.blit(difficultydisplay, (self.pfpx, self.pfpy + 125))
        if self.rectleft.collidepoint(mousepos):
            if mousepress[0] and self.difficulty > 0 and cooldown("arrow_left", 0.5):
                self.difficulty -= 1
        if self.rectright.collidepoint(mousepos):
            if mousepress[0] and self.difficulty < 10 and cooldown("arrow_right", 0.5):
                self.difficulty += 1
    
    def reset(self):
        self.difficulty = 0

    def update(self):
        self.arrowdisplay()
#==================================================================================================#

#Groups
customenemygroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
#==================================================================================================#

# Mainscreen
def mainscreen(screen):
    vhs(screen)
    screen.blit(title, (200, 200))
    screen.blit(playbutton, playbuttonrect)
    screen.blit(quitbutton, quitbuttonrect)
    screen.blit(optionsbutton, optionsbuttonrect)
    screen.blit(charliepfp, (1200, 600))
    
    mousepos = pygame.mouse.get_pos()
    mousepress = pygame.mouse.get_pressed()
    
    if playbuttonrect.collidepoint(mousepos):
        screen.blit(playbuttonp, playbuttonrect)
        if mousepress[0]:
            States.append(customscreen)
    if optionsbuttonrect.collidepoint(mousepos):
        screen.blit(optionsbuttonp, optionsbuttonrect)
    if quitbuttonrect.collidepoint(mousepos):
        screen.blit(quitbuttonp, quitbuttonrect)
        if mousepress[0]:
            pygame.quit()
            exit()
#==================================================================================================#
# Custom Enemies

customenemygroup.add(CustomEnemy("Coby", 0, pygame.image.load("Data/States/Custom/Coby.png"), 530, 250))
customenemygroup.add(CustomEnemy("Chavo", 0, pygame.image.load("Data/States/Custom/Chavo.png"), 770, 250))
customenemygroup.add(CustomEnemy("Frederick", 0, pygame.image.load("Data/States/Custom/Frederick.png"), 1010, 250))
customenemygroup.add(CustomEnemy("Cody", 0, pygame.image.load("Data/States/Custom/Cody.png"), 530, 510))
customenemygroup.add(CustomEnemy("FredDerick", 0, pygame.image.load("Data/States/Custom/Fred_Derrick.png"), 770, 510))
customenemygroup.add(CustomEnemy("Cedrick", 0, pygame.image.load("Data/States/Custom/Cedrick.png"), 1010, 510))


#Real Enemies

class Coby(Enemy):
    def __init__(self, name, diffculty, pathing, jumpscare, posarray):
        super().__init__(name, diffculty)
        self.rest = pygame.image.load("Data/Characters/Coby/CobyRest.png")
        self.hall = pygame.image.load("Data/Characters/Coby/CobyHall.png")
        self.wall = pygame.image.load("Data/Characters/Coby/CobyWall.png")
        self.office = pygame.image.load("Data/Characters/Coby/CobyIn.png")
        self.jumpscare = imgimport("Data/Characters/Coby/CobyJumpscare.png", (1920, 1080))
        self.image = self.rest

    def movement(self):
        pass

enemygroup.add(Coby("Coby", 0, 0, 0, 0))
#==================================================================================================#
# Customscreen
def customscreen(screen):
    vhs(screen)
    screen.blit(customborders, (360, 90))
    screen.blit(backbutton, backbuttonrect)
    screen.blit(beginbutton, beginbuttonrect)
    customenemygroup.draw(screen)
    customenemygroup.update()
    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0]:
            States.pop()
    if beginbuttonrect.collidepoint(mousepos):
        screen.blit(beginbuttonp, beginbuttonrect)
        if mousepress[0]:
            States.append(game)

# Game Map

office = imgimport("Data/States/Map/Office.png", (1920, 1080))
back = imgimport("Data/States/Map/Back.png", (1920, 1080))
dark = imgimport("Data/States/Mechanics/Dark.png", (1920, 1080))
coop = imgimport("Data/States/Map/Coop.png", (1920, 1080))
lwall = imgimport("Data/States/Map/LeftWall.png", (1920, 1080))
lhall = imgimport("Data/States/Map/LeftHall.png", (1920, 1080))
rwall = imgimport("Data/States/Map/RightWall.png", (1920, 1080))
rhall = imgimport("Data/States/Map/RightHall.png", (1920, 1080))
uwall = imgimport("Data/States/map/UpWall.png", (1920, 1080))
uhall = imgimport("Data/States/Map/UpHall.png", (1920, 1080))
fhall = imgimport("Data/States/Map/FrontHall.png", (1920, 1080))

#mechanics

flashlight = pygame.image.load("Data/States/Mechanics/Flashlight.png")
rdoor = imgimport("Data/States/Mechanics/RDoor.png", (1920, 1080))
ldoor = imgimport("Data/States/Mechanics/LDoor.png", (1920, 1080))


# Gameplay variables
inoffice = True
flashlighton = False
flashlightpos = (-1000, -600)
incameras = False
camerapos = 1
cameraposarray = [0, lwall, lhall, coop, rhall, rwall, fhall, uhall, uwall]
inback = False

# Camera function
def numcam():
    global camerapos
    if keys[pygame.K_1]:
        camerapos = 1
    if keys[pygame.K_2]:
        camerapos = 2
    if keys[pygame.K_3]:
        camerapos = 3
    if keys[pygame.K_4]:
        camerapos = 4
    if keys[pygame.K_5]:
        camerapos = 5
    if keys[pygame.K_6]:
        camerapos = 6
    if keys[pygame.K_7]:
        camerapos = 7
    if keys[pygame.K_8]:
        camerapos = 8

#Door Variables
drpos = -500
dlpos = -500
dlclosed = False
drclosed = False

#Door Function
def door(side):
    global drpos, dlpos, dlclosed, drclosed
    if side == "r":
        if drclosed:
            drpos = -500
            drclosed = False
        else:
            drpos = 0
            drclosed = True
    if side == "l":
        if dlclosed:
            dlpos = -500
            dlclosed = False
        else:
            dlpos = 0
            dlclosed = True

# Game
def game(screen):
    global inoffice, flashlighton, flashlightpos, incameras, inback
    if inoffice:
        screen.fill((0, 0, 0))
        screen.blit(rdoor, (0, drpos))
        screen.blit(ldoor, (0, dlpos))
        screen.blit(office, (0, 0))
        if keys[pygame.K_q] and cooldown("ldoor", 0.5):
            door("l")
        if keys[pygame.K_e] and cooldown("rdoor", 0.5):
            door("r")
        if keys[pygame.K_SPACE] and not flashlighton and cooldown("flashlight", 0.2):
            flashlighton = True
        if keys[pygame.K_SPACE] and flashlighton and cooldown("flashlight", 0.2):
            flashlighton = False
        if keys[pygame.K_s]:
            flashlightpos = (-1000, -600)#-1400, -1000
        if keys[pygame.K_a]:
            flashlightpos = (-1700, -500)
        if keys[pygame.K_d]:
            flashlightpos = (-230, -500)
        if keys[pygame.K_w]:
            flashlightpos = (-1400, -1000)
        if keys[pygame.K_c] and cooldown("cameras", 0.2):
            incameras = True
            inoffice = False
        if keys[pygame.K_x] and cooldown("back", 0.2):
            inback = True
            inoffice = False
        if not flashlighton:
            screen.blit(dark, (0, 0))
        if flashlighton:
            screen.blit(flashlight, flashlightpos)
    if incameras:
        screen.fill((0, 0, 0))
        numcam()
        screen.blit(cameraposarray[camerapos], (0, 0))
        if camerapos != 6:
            rain(screen)
        screen.blit(dark, (0, 0))
        if keys[pygame.K_c] and cooldown("cameras", 0.2):
            inoffice = True
            incameras = False
    if inback:
        screen.fill((0, 0, 0))
        screen.blit(back, (0, 0))
        screen.blit(dark, (0, 0))
        if keys[pygame.K_x] and cooldown("back", 0.2):
            inoffice = True
            inback = False
    enemygroup.update()
# Main loop
States = [mainscreen]

while True:
    mousepos = pygame.mouse.get_pos()
    mousepress = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    time2dp = round(time.time(),2)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Call the current state function
    States[-1](screen)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)