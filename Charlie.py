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
rawtime = int(time.time())
#==================================================================================================#
#LAST DONE:
#balanced the power and tick for enemies
#power and time displays no matter what gamestate you are in
#cody and coby are now fully functional
#reduce custom arrow cooldown

#TO ADD:
#Cedrick the fat chicken
#

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
        self.ticktime = 0
        self.jumpscare = None
        self.inside = False
        self.inside_time = 0  # Add this line
        self.cankill = False
    def iskilled(self):
        pass

    def killplayer(self):
        global jumpscaretimer
        if self.cankill:
            screen.blit(self.jumpscare, (0, 0))
            jumpscaretimer += 1
            if jumpscaretimer >= 60:
                states.append(lose)

    def tick(self):
        global jumpscaretimer
        if self.pos == 0:
            self.flashlight_sight()
        if cooldown(self.name, self.ticktime):
            if self.diffculty > random.randint(0, 10):
                self.move()

    def move(self):
        if self.pos != 0 and self.pos != 3:
            if self.diffculty > random.randint(-10, 10):
                currentpos = self.pathing.index(self.pos) + 1
                self.pos = self.pathing[currentpos]
                self.image = self.imagearray[currentpos]
            else:
                currentpos = self.pathing.index(self.pos) - 1
                self.pos = self.pathing[currentpos]
                self.image = self.imagearray[currentpos]
        else:
                currentpos = self.pathing.index(self.pos) + 1
                self.pos = self.pathing[currentpos]
                self.image = self.imagearray[currentpos]


    def display(self):
        global camerapos, incameras
        if camerapos == self.pos and incameras:
            screen.blit(self.image, self.screenpos)
        if self.pos == 0 and not incameras:
            screen.blit(self.image, self.screenpos)
    
    def positionswitch(self):
        pass
    
    def flashlight_sight(self):
        global flashlightpos, flashlighton
        if flashlightpos == self.flashlight and flashlighton:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        

    def update(self):
        self.display()
        self.tick()
        self.positionswitch()
        self.killplayer()



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
            if mousepress[0] and self.difficulty > 0 and cooldown("arrow_left", 0.2):
                self.difficulty -= 1
        if self.rectright.collidepoint(mousepos):
            if mousepress[0] and self.difficulty < 10 and cooldown("arrow_right", 0.2):
                self.difficulty += 1
    def returndifficulty(self):
        return self.difficulty

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
            states.append(customscreen)
    if optionsbuttonrect.collidepoint(mousepos):
        screen.blit(optionsbuttonp, optionsbuttonrect)
        if mousepress[0]:
            states.append(options)
    if quitbuttonrect.collidepoint(mousepos):
        screen.blit(quitbuttonp, quitbuttonrect)
        if mousepress[0]:
            pygame.quit()
            exit()
#==================================================================================================#

# Options
def options(screen):
    vhs(screen)
    screen.blit(backbutton, backbuttonrect)
    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0]:
            states.pop()

#==================================================================================================#

# Custom Enemies
cobybutton = CustomEnemy("Coby", 0, pygame.image.load("Data/States/Custom/Coby.png"), 530, 250)
customenemygroup.add(cobybutton)
codybutton = CustomEnemy("Cody", 0, pygame.image.load("Data/States/Custom/Cody.png"), 530, 510)
customenemygroup.add(codybutton)
cedrickbutton = CustomEnemy("Cedrick", 0, pygame.image.load("Data/States/Custom/Cedrick.png"), 1010, 510)
customenemygroup.add(cedrickbutton)
customenemygroup.add(CustomEnemy("Chavo", 0, pygame.image.load("Data/States/Custom/Chavo.png"), 770, 250))
customenemygroup.add(CustomEnemy("Frederick", 0, pygame.image.load("Data/States/Custom/Frederick.png"), 1010, 250))
customenemygroup.add(CustomEnemy("FredDerick", 0, pygame.image.load("Data/States/Custom/Fred_Derrick.png"), 770, 510))



#Real Enemies

class Coby(Enemy):
    def __init__(self, name, diffculty):
        super().__init__(name, diffculty)
        self.rest = pygame.image.load("Data/Characters/Coby/CobyRest.png")
        self.hall = pygame.image.load("Data/Characters/Coby/CobyHall.png")
        self.wall = pygame.image.load("Data/Characters/Coby/CobyWall.png")
        self.office = imgimport("Data/Characters/Coby/CobyIn.png", (200, 200))
        self.jumpscare = imgimport("Data/Characters/Coby/CobyJumpscare.png", (1920, 1080))
        self.image = self.rest
        self.pathing = [3, 2 , 1, 0]
        self.imagearray = [self.rest, self.hall, self.wall, self.office]
        self.ticktime = 1
        self.flashlight = (-1700, -500)
        self.screenpos = (400, 400)

    def move(self):
        global inplay
        if self.pos == 0:
            if dlclosed:
                self.pos = 3
                self.image = self.rest
            if not dlclosed:
                self.cankill = True
        else:
            super().move()
    
    def positionswitch(self):
        if self.pos != 0:
            self.screenpos = (400, 400)
        else:
            self.screenpos = (10, 400)


class Cody(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/Cody/CodyRest.png")
        self.hall = pygame.image.load("Data/Characters/Cody/CodyHall.png")
        self.wall = pygame.image.load("Data/Characters/Cody/CodyWall.png")
        self.office = imgimport("Data/Characters/Cody/CodyIn.png", (200, 200))
        self.jumpscare = imgimport("Data/Characters/Cody/CodyJumpscare.png", (1920, 1080))
        self.image = self.rest
        self.pathing = [3, 4 , 5, 0]
        self.imagearray = [self.rest, self.hall, self.wall, self.office]
        self.ticktime = 1
        self.flashlight = (-230, -500)
        self.screenpositon = (800, 400)

    def move(self):
        global inplay
        if self.pos == 0:
            if drclosed:
                self.pos = 3
                self.image = self.rest
            if not drclosed:
                self.cankill = True
        else:
            super().move()

    def positionswitch(self):
        if self.pos != 0:
            self.screenpos = (800, 400)
        else:
            self.screenpos = (1600, 400)

class Cedrick(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/Cedrick/CedrickRest.png")
        self.hall = pygame.image.load("Data/Characters/Cedrick/CedrickHall.png")
        self.office = imgimport("Data/Characters/Cedrick/CedrickIn.png", (200, 200))
        self.jumpscare = imgimport("Data/Characters/Cedrick/CedrickJumpscare.png", (1920, 1080))
        self.image = self.rest
        self.pathing = [3, 6, 0]
        self.imagearray = [self.rest, self.hall, self.office]
        self.ticktime = 1
        self.flashlight = (-1000, -600)
        self.screenpositon = (200, 400)
        self.activated = False
        self.flashlight_time = 0

    def move(self):
        global inplay
        if self.pos == 6:
            self.activated = True
            super().move()
        elif self.pos == 0:
            if not self.activated:
                self.pos = 3
                self.image = self.rest
            if self.activated:
                self.cankill = True
        else:
            super().move()
    def flashlight_sight(self):
        if flashlightpos == self.flashlight and flashlighton:
            self.flashlight_time += 1
            self.cankill = False
        print(self.cankill)
        if self.flashlight_time >= 200:
            self.activated = False
            self.flashlight_time = 0
        super().flashlight_sight()
    def positionswitch(self):
        if self.pos != 0:
            self.screenpos = (800, 400)
        else:
            self.screenpos = (1000, 400)
 
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
            states.pop()
    if beginbuttonrect.collidepoint(mousepos):
        screen.blit(beginbuttonp, beginbuttonrect)
        if mousepress[0]:
            reset()
            enemygroup.add(Coby("Coby", cobybutton.returndifficulty()))
            enemygroup.add(Cody("Cody", codybutton.returndifficulty()))
            enemygroup.add(Cedrick("Cedrick", cedrickbutton.returndifficulty()))
            states.append(game)

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
power = 20000
inplay = False
jumpscaretimer = 0

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
#Reset game variables function

def reset():
    global inoffice, incameras, inback, flashlighton, flashlightpos, incameras, inback, power, rawtime, inplay, jumpscaretimer
    jumpscaretimer = 0
    inoffice = True
    flashlighton = False
    incameras = False
    inback = False
    flashlightpos = (-1000, -600)
    incameras = False
    inback = False
    power = 40000
    rawtime = int(time.time())
    inplay = True
    enemygroup.empty()

# Game
def game(screen):
    global inoffice, flashlighton, flashlightpos, incameras, inback, power, rawtime
    power -= 2
    powerdisplay = powerfont.render(str(power//200)+"%", True, "White")
    elapsed_time = (int(time.time()) - rawtime) * 2  # Double the elapsed time
    if (elapsed_time // 60) >= 1:
        TimeDisplay = powerfont.render("TIME: " + str(elapsed_time // 60) + "AM", True, "White")
    else:
        TimeDisplay = powerfont.render("TIME: " + str((elapsed_time // 60) + 12) + "AM", True, "White")
    if dlclosed:
        power -=10
    if drclosed:
        power -=10
    if inoffice:
        screen.fill((0, 0, 0))
        screen.blit(office, (0, 0))
        enemygroup.update()
        if drclosed:
            screen.blit(rdoor, (0, drpos))
        if dlclosed:
            screen.blit(ldoor, (0, dlpos))
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
            power -= 5
    if (elapsed_time // 60) == 6:
        states.append(win)
    if power <= 0:
        states.append(lose)
    if incameras:
        screen.fill((0, 0, 0))
        numcam()
        screen.blit(cameraposarray[camerapos], (0, 0))
        enemygroup.update()
        if camerapos != 6:
            rain(screen)
        screen.blit(dark, (0, 0))
        if keys[pygame.K_c] and cooldown("cameras", 0.2):
            inoffice = True
            incameras = False
    if inback:
        screen.fill((0, 0, 0))
        screen.blit(back, (0, 0))
        enemygroup.update()
        screen.blit(dark, (0, 0))
        if keys[pygame.K_x] and cooldown("back", 0.2):
            inoffice = True
            inback = False
    screen.blit(powerdisplay,(0,1000))
    screen.blit(TimeDisplay, (0,0))
    

# Win Screen
def win(screen):
    screen.fill((0, 0, 0))
    vhs(screen)
    win = powerfont.render("You Win (Press space to return to menu)", True, "White")
    screen.blit(win, center)
    if keys[pygame.K_SPACE]:
        states.pop()
        states.pop()
        states.pop()

# Lose Screen
def lose(screen):
    screen.fill((0, 0, 0))
    vhs(screen)
    lose = powerfont.render("You Lose (Press space to return to menu)", True, "White")
    screen.blit(lose, center)
    if keys[pygame.K_SPACE]:
        states.pop()
        states.pop()
        states.pop()
# Main loop
states = [mainscreen]

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
    states[-1](screen)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)