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
canpress = True
cooldowntimer = 0
#Cooldowwn function
def cooldown(seconds):
    global canpress, cooldowntimer
    canpress = False
    while canpress == False:
        cooldowntimer += 1
        if cooldowntimer >= seconds * 600:
            canpress = True
            cooldowntimer = 0
            break

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
    def __init__(self, name, diffculty, pathing, jumpscare, posarray):
        super().__init__()
        self.name = name
        self.diffculty = diffculty
        self.pathing = pathing
        self.jumpscare = jumpscare
        self.posarray = posarray

    
    def update(self):
        pass

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
        global canpress
        screen.blit(arrowl, self.rectleft)
        screen.blit(arrowr, self.rectright)
        difficultydisplay = powerfont.render(str(self.difficulty), True, "White")
        screen.blit(difficultydisplay, (self.pfpx, self.pfpy + 125))
        if self.rectleft.collidepoint(mousepos):
            if mousepress[0] and self.difficulty > 0 and canpress:
                self.difficulty -= 1
                cooldown(60)
        if self.rectright.collidepoint(mousepos):
            if mousepress[0] and self.difficulty < 10 and canpress:
                self.difficulty += 1
                cooldown(60)
    
    def reset(self):
        self.difficulty = 0

    def update(self):
        self.arrowdisplay()
#==================================================================================================#

#Groups
customenemygroup = pygame.sprite.Group()
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



#==================================================================================================#
# Customscreen
def customscreen(screen):
    vhs(screen)
    screen.blit(customborders, (360, 90))
    screen.blit(backbutton, backbuttonrect)
    screen.blit(beginbutton, beginbuttonrect)
    customenemygroup.draw(screen)
    customenemygroup.update()
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
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Call the current state function
    States[-1](screen)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)