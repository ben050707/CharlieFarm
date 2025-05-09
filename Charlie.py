import pygame
import random
import time
import os
import Database
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Charlie's Farm")
clock = pygame.time.Clock()
powerfont = pygame.font.Font(None, 50)
center = (600, 450)
transparent = (0, 0, 0, 0)
rawtime = int(time.time())
dying = False
current_user = None
current_star = 0
customgame = False
final_score = 0
flashlevel = 0
canpurchase = True
powermultiplier = 1
generated_code = None
#==================================================================================================#
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
    VHS.append(pygame.image.load(f"./Data/States/Mainscreen/VHS/{i}.png"))

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

def debug_win():
    global states
    # Simulate winning the game
    states.append(win)

def display_stars(screen, star_count):

    #Display the user's stars in a row on the screen.

    #param screen: The Pygame screen surface.
    #param star_count: The number of stars the user has.

    star_image = pygame.image.load("Data/States/Mainscreen/star.png")  # Load the star image
    star_image = pygame.transform.scale(star_image, (50, 50))  # Resize the star image if needed
    star_spacing = 60  # Space between each star

    for i in range(star_count):
        screen.blit(star_image, (150 + i * star_spacing, 400))  # Display stars in a row
#-------------------------------------------------------------------------------------------------#

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

controlsbutton = pygame.image.load("Data/States/Mainscreen/Controlsbutton.png")
controlsbuttonp = pygame.image.load("Data/States/Mainscreen/ControlsbuttonP.png")
controlsbuttonrect = controlsbutton.get_rect(center = (800, 750))

charliepfp = pygame.image.load("Data/States/Mainscreen/Charlie.png")

stardisplay = pygame.image.load("Data/States/Mainscreen/star.png")
#--------------------------------------------------------------------------------------------------#

#Playbuttons

newgamebutton = pygame.image.load("data/states/play/newgamebutton.png")
newgamebuttonp = pygame.image.load("data/states/play/newgamebuttonp.png")
newgamebuttonrect = newgamebutton.get_rect(center = (300, 600))

continuebutton = pygame.image.load("data/states/play/continuebutton.png")
continuebuttonp = pygame.image.load("data/states/play/continuebuttonp.png")
continuebuttonrect = continuebutton.get_rect(center = (300, 750))

custombutton = pygame.image.load("data/states/play/custombutton.png")
custombuttonp = pygame.image.load("data/states/play/custombuttonp.png")
custombuttonrect = custombutton.get_rect(center = (300, 900))

# Define difficulty progression for each character based on stars
difficulty_progression = {
    "Coby": [1, 2, 3, 6, 7, 8],  # Difficulty increases with stars
    "Cody": [1, 2, 4, 5, 6, 8],
    "Cedrick": [0, 1, 2, 3, 4, 8],
    "Chavo": [0, 0, 2, 3, 4, 8],
    "Frederick": [0, 0, 0, 2, 3, 8],
    "FredDerick": [0, 1, 2, 3, 4, 8],
}

#--------------------------------------------------------------------------------------------------#

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

#--------------------------------------------------------------------------------------------------#

#Options buttons

registerbutton = pygame.image.load("data/states/Options/registerbutton.png")
registerbuttonp = pygame.image.load("data/states/Options/registerbuttonp.png")
registerbuttonrect = registerbutton.get_rect(topleft = (500, 900))

loginbutton = pygame.image.load("data/states/Options/loginbutton.png")
loginbuttonp = pygame.image.load("data/states/Options/loginbuttonp.png")
loginbuttonrect = loginbutton.get_rect(center = (300, 600))

logoutbutton = pygame.image.load("data/states/Options/logoutbutton.png")
logoutbuttonp = pygame.image.load("data/states/Options/logoutbuttonp.png")
logoutbuttonrect = logoutbutton.get_rect(center = (300, 750))

leaderboardbutton = pygame.image.load("data/states/Options/leaderboardbutton.png")
leaderboardbuttonp = pygame.image.load("data/states/Options/leaderboardbuttonp.png")
leaderboardbuttonrect = leaderboardbutton.get_rect(center = (300, 900))



optionsbackbuttonrect = backbutton.get_rect(topleft = (600, 850))
loginscreenbuttonrect = loginbutton.get_rect(topleft = (1000, 900))

logingui = imgimport("data/states/Options/logingraphic.png", (1920, 1080))

usernamerect = pygame.rect.Rect(500, 350, 840, 140)
passwordrect = pygame.rect.Rect(500, 725, 840, 140)
#--------------------------------------------------------------------------------------------------#

#Shop buttons

shopbutton = pygame.image.load("data/states/shop/shopbutton.png")
shopbuttonp = pygame.image.load("data/states/shop/shopbuttonp.png")
shopbuttonrect = shopbutton.get_rect(center = (600, 600))

buybutton = pygame.image.load("data/states/shop/buybutton.png")
buybuttonp = pygame.image.load("data/states/shop/buybuttonp.png")
canbuy = pygame.image.load("data/states/shop/buybutton.png")
cantbuy = pygame.image.load("data/states/shop/expensive.png")
buybuttonrect = buybutton.get_rect(center = (890, 550))

bat1 = pygame.image.load("data/states/shop/bat1.png")
bat2 = pygame.image.load("data/states/shop/bat2.png")
bat3 = pygame.image.load("data/states/shop/bat3.png")
soldout = pygame.image.load("data/states/shop/soldout.png")

#--------------------------------------------------------------------------------------------------#

#Controls buttons

leftbutton = pygame.image.load("data/states/Options/left.png")
leftbuttonrect = leftbutton.get_rect(center = (300, 600))

rightbutton = pygame.image.load("data/states/Options/right.png")
rightbuttonrect = rightbutton.get_rect(center = (300, 700))
ControlIndex = 0
Entity = ["State: Office", "State: Cameras", "State: Back", "Entity: Coby", "Entity: Cody","Entity: Frederick", "Entity: Chavo", "Entity: Cedrick", "Entity: FredDerick"]
PFP = [0, 0, 0, pygame.image.load("Data/States/Custom/Coby.png"), pygame.image.load("Data/States/Custom/Cody.png"), pygame.image.load("Data/States/Custom/Frederick.png"),
        pygame.image.load("Data/States/Custom/Chavo.png"), pygame.image.load("Data/States/Custom/Cedrick.png"), pygame.image.load("Data/States/Custom/Fred_Derrick.png")
        ]
for i in range(len(PFP)):
    if PFP[i] != 0:
        PFP[i] = pygame.transform.scale(PFP[i], (400, 400))

Description = [
    #Office
    "You have a power meter and a time limit. To beat the game, you must reach 6AM before you get caught by one \n"
    "of the enemies or before your power runs out.\n"
    "You press SPACEBAR to turn on/off your flashlight and WASD to move it.\n"
    "Use Q/E to toggle the doors on and off. Keep in mind using the flashlight or the doors will drain your power. \n"
    "Use C to enter the camera state. \n"
    "Use B to enter the backview state.",
    #Cameras
    "In this state, you are able to look through the cameras, revealing the locations of the enemies. \n"
    "You can use numbers 1-9 to change between camera positions. \n"
    "You are vulnerable to the enemies in this state, and it slowly drains your power, so only use it when necessary. \n"
    "Use C to exit out of the camera state back into the office state",
    #Back
    "In this state, you are able to look through the backview, checking the status of the minigame. \n"
    "You are vulnerable to the enemies in this state, so only enter this state when necessary. \n"
    "Use B to exit out of the backview state and back into the office state",
    #Coby
    "Coby is an enemy that will slowly move towards you. \n"
    "He occupies the left side door, to get rid of Coby, you press Q to toggle the door shut. He will eventually leave, \n" 
    "returning to his original position. \n"
    "There is a small chance for all enemies(excluding FredDerick) to move backwards from their path. \n"
    "If you do not press Q in time, you will get caught by Coby and the game will end.",
    #Cody
    "Cody is an enemy that will slowly move towards you. \n"
    "He occupies the right side door, to get rid of Cody, you press E to toggle the door shut. He will eventually leave, \n"
    "returning to his original position. \n"
    "If you do not press E in time, you will get caught by Cody and the game will end.",
    #Frederick
    "Frederick is not a physical entity but instead is a character made to make it harder to deal with other enemies. \n"
    "He will hack your cameras, preventing you from using them. \n"
    "To undo this hack, you must find the camera position containing a change in the hack image(red text) \n"
    "Cedrick's movement is impeded by camera view, so if the cameras are hacked he is free to move around. \n",
    #Chavo
    "Chavo is an enemy that moves towards the front side of the barn. \n"
    "There is a camera position that does not display anything, but you can hear if Chavo is there. \n"
    "If Chavo is seen in the office, you must use the flashlight to blind him for a certain period of time. \n"
    "Chavo will return to his original position if you have blinded him for long enough. \n"
    "If you do not blind Chavo in time, you will get caught by Chavo and the game will end.",
    #Cedrick
    "Cedrick is an enemy that will not enter the office directly but can still catch you. \n"
    "He will move towards the upstairs of the barn, then move to the right side of the barn. \n"
    "If you see him on the cameras on the right side of the barn, you must press E to toggle the right door shut. \n"
    "If you do not press E in time, you will get caught by Cedrick and the game will end."
    "If you do shut the door in time, Cedrick will return to his original position.",
    #FredDerick
    "FredDerick is the only enemy that does not start in the chicken coop, but is instead trapped inside the shed. \n"
    "There are ropes blocking the door, preventing FredDerick from escaping. \n"
    "The ropes will begin to snap, so you must match the colors to secure the ropes again. \n"
    "The ropes will not snap if you are viewing the backview. \n"
    "If all the ropes snap, All the ropes will reconnnect and FredDerick will increase in anger. \n"
    "If all the ropes have snapped 3 times, FredDerick will instantly end the game."
]

def render_multiline_text(screen, text_array, index, font, color, x, y, line_height):
    
    #Render a specific paragraph from a list of multi-line text on the screen.

    #:param screen: The Pygame screen surface.
    #:param text_array: A list of multi-line text strings.
    #:param index: The index of the paragraph to display.
    #:param font: The Pygame font object.
    #:param color: The color of the text.
    #:param x: The x-coordinate of the starting position.
    #:param y: The y-coordinate of the starting position.
   #:param line_height: The vertical space between lines.

    if 0 <= index < len(text_array):  # Ensure the index is valid
        text = text_array[index]  # Get the specific paragraph
        lines = text.split("\n")  # Split the text into lines
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x, y + i * line_height))
    else:
        print(f"Index {index} is out of range for the text array.")
#--------------------------------------------------------------------------------------------------#
#Database configuration
#==================================================================================================#
class keyboard:
    def __init__(self):
        self.letter_array = []
        self.word = ""
        self.can_type = True
        self.type_marker_timer = 0
        self.focus = False  # Tracks whether this input field is active

    def backspace(self):
        if len(self.letter_array) > 0:
            self.letter_array.pop()

    def add(self, input):
        if self.can_type and self.focus:  # Only process input if this field is focused
            if (input >= 97 and input <= 122) or (input >= 48 and input <= 57):  # Letters and numbers
                self.type(input)
            if input == 8:  # Backspace
                self.backspace()

    def type(self, input):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        typekey = ""
        if input >= 97 and input <= 122:  # Letters
            input -= 97
            typekey = letters[input]
        if input >= 48 and input <= 57:  # Numbers
            input -= 48
            typekey = numbers[input]

        self.letter_array.append(typekey)

    def display(self, rect):
        username = ""
        for letter in self.letter_array:
            username += letter

        display_name = pygame.font.Font.render(powerfont, username, False, "White")
        display_name_rect = display_name.get_rect(center=rect.center)
        if display_name_rect.width > rect.width - 180:
            self.can_type = False
        else:
            self.can_type = True
        screen.blit(display_name, display_name_rect)

        # Display the type marker (blinking cursor) only if this field is focused
        if self.focus:
            type_marker = pygame.font.Font.render(powerfont, "|", False, "Grey")
            self.type_marker_timer += 0.01
            if self.type_marker_timer >= 2:
                screen.blit(type_marker, (display_name_rect.topright))
            if self.type_marker_timer >= 4:
                self.type_marker_timer = 0

    def get_word(self):
        self.word = "".join(self.letter_array)
        return self.word

usernameinput = keyboard()
passwordinput = keyboard()
# Character Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, difficulty):
        super().__init__()
        self.name = name
        self.difficulty = difficulty
        self.pos = 3
        self.image = None
        self.ticktime = 0
        self.jumpscare = None
        self.inside = False
        self.inside_time = 0  # Variable to track inside time
        self.cankill = False
    def iskilled(self):
        pass

    def killplayer(self):
        global jumpscaretimer, dying,inback,incameras,inoffice
        
        if self.cankill:
            inoffice = True
            incameras = False
            inback = False
            if type(self.jumpscare) is list:
                dying = True
                self.jumpscarelength = len(self.jumpscare) * 10
                screen.blit(self.jumpscare[jumpscaretimer//10], (0, 0))
                jumpscaretimer += 1
                if jumpscaretimer >= self.jumpscarelength:
                    dying = False
                    states.append(lose)
            else:
                dying = True
                screen.blit(self.jumpscare, (0, 0))
                jumpscaretimer += 1
                if jumpscaretimer >= 60:
                    dying = False
                    states.append(lose)

    def tick(self):
        global jumpscaretimer
        if self.pos == 0:
            self.flashlight_sight()
        if cooldown(self.name, self.ticktime):
            if self.difficulty > random.randint(0, 20):
                self.move()

    def move(self):
        if self.pos != self.pathing[0] and self.pos != self.pathing[len(self.pathing)-1]:
            if self.difficulty > random.randint(-20, 10):
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
        if camerapos == self.pos and incameras and not hacked:
            screen.blit(self.image, self.screenpos)
        if self.pos == 0 and not incameras:
            self.flashlight_sight()
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


# Custom Enemy Class
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
            if mousepress[0] and self.difficulty > 0 and cooldown("arrow_left", 0.1):
                self.difficulty -= 1
        if self.rectright.collidepoint(mousepos):
            if mousepress[0] and self.difficulty < 10 and cooldown("arrow_right", 0.1):
                self.difficulty += 1
    def returndifficulty(self):
        return self.difficulty

    def reset(self):
        self.difficulty = 0

    def update(self):
        self.arrowdisplay()
#--------------------------------------------------------------------------------------------------#

#Groups
customenemygroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
#==================================================================================================#

# Mainscreen
def mainscreen(screen):
    global current_user

    vhs(screen)
    screen.blit(title, (200, 200))
    screen.blit(playbutton, playbuttonrect)
    screen.blit(quitbutton, quitbuttonrect)
    screen.blit(optionsbutton, optionsbuttonrect)
    screen.blit(charliepfp, (1200, 600))
    screen.blit(shopbutton, shopbuttonrect)
    screen.blit(controlsbutton, controlsbuttonrect)

    mousepos = pygame.mouse.get_pos()
    mousepress = pygame.mouse.get_pressed()
    
        # Display the user's stars if logged in
    if current_user:
        star_count = Database.get_stars()
        display_stars(screen, star_count)

    if shopbuttonrect.collidepoint(mousepos):
        screen.blit(shopbuttonp, shopbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            states.append(shop)
        
    if playbuttonrect.collidepoint(mousepos):
        screen.blit(playbuttonp, playbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            states.append(play)

    if optionsbuttonrect.collidepoint(mousepos):
        screen.blit(optionsbuttonp, optionsbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            states.append(options)

    if controlsbuttonrect.collidepoint(mousepos):
        screen.blit(controlsbuttonp, controlsbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            states.append(controls)

    if quitbuttonrect.collidepoint(mousepos):
        screen.blit(quitbuttonp, quitbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            if current_user != None:
                Database.logout_user()
                current_user = None  # Reset the current user
            pygame.quit()
            exit()
#--------------------------------------------------------------------------------------------------#
def play(screen):
    global current_star, customgame
    vhs(screen)

    # Get the current user's stars
    current_star = Database.get_stars()

    # Display buttons

    screen.blit(newgamebutton, newgamebuttonrect)
    screen.blit(continuebutton, continuebuttonrect)
    screen.blit(custombutton, custombuttonrect)
    screen.blit(backbutton, optionsbackbuttonrect)

    star_count = Database.get_stars()
    if current_user:
        display_stars(screen, star_count)
    # Handle button clicks
    if newgamebuttonrect.collidepoint(mousepos):
        screen.blit(newgamebuttonp, newgamebuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            customgame = False # Set customgame to False
            # Reset the user's stars to 0
            Database.change_stars(-current_star)  # Subtract current stars to set to 0
            current_star = 0  # Update the current_star variable

            # Set the difficulty based on stars (0 in this case)
            coby_difficulty = difficulty_progression["Coby"][current_star]
            cody_difficulty = difficulty_progression["Cody"][current_star]
            cedrick_difficulty = difficulty_progression["Cedrick"][current_star]
            chavo_difficulty = difficulty_progression["Chavo"][current_star]
            frederick_difficulty = difficulty_progression["Frederick"][current_star]
            fredderick_difficulty = difficulty_progression["FredDerick"][current_star]

            # Initialize the game with the calculated difficulties
            reset()
            enemygroup.add(Coby("Coby", coby_difficulty))
            enemygroup.add(Cody("Cody", cody_difficulty))
            enemygroup.add(Cedrick("Cedrick", cedrick_difficulty))
            enemygroup.add(Chavo("Chavo", chavo_difficulty))
            enemygroup.add(Frederick("Frederick", frederick_difficulty))
            enemygroup.add(FredDerick("FredDerick", fredderick_difficulty))

            # Start the game
            states.append(game)

    if continuebuttonrect.collidepoint(mousepos):
        screen.blit(continuebuttonp, continuebuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            customgame = False # Set customgame to False
            # Use the user's current stars to set the difficulty
            coby_difficulty = difficulty_progression["Coby"][current_star]
            cody_difficulty = difficulty_progression["Cody"][current_star]
            cedrick_difficulty = difficulty_progression["Cedrick"][current_star]
            chavo_difficulty = difficulty_progression["Chavo"][current_star]
            frederick_difficulty = difficulty_progression["Frederick"][current_star]
            fredderick_difficulty = difficulty_progression["FredDerick"][current_star]

            # Initialize the game with the calculated difficulties
            reset()
            enemygroup.add(Coby("Coby", coby_difficulty))
            enemygroup.add(Cody("Cody", cody_difficulty))
            enemygroup.add(Cedrick("Cedrick", cedrick_difficulty))
            enemygroup.add(Chavo("Chavo", chavo_difficulty))
            enemygroup.add(Frederick("Frederick", frederick_difficulty))
            enemygroup.add(FredDerick("FredDerick", fredderick_difficulty))

            # Start the game
            states.append(game)

    if custombuttonrect.collidepoint(mousepos):
        screen.blit(custombuttonp, custombuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            customgame = True
            states.append(customscreen)

    if optionsbackbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, optionsbackbuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            states.pop()
#--------------------------------------------------------------------------------------------------#
def controls(screen):
    global ControlIndex

    vhs(screen)
    # Display the left and right buttons
    screen.blit(leftbutton, leftbuttonrect)
    screen.blit(rightbutton, rightbuttonrect)
    screen.blit(backbutton, backbuttonrect)

    # Display the entity and description
    Title = powerfont.render(Entity[ControlIndex], True, "White")
    screen.blit(Title, (800, 50))
    if PFP[ControlIndex] != 0:
        screen.blit(PFP[ControlIndex], (1300, 600))

    # Render the description directly
    render_multiline_text(screen, Description, ControlIndex, powerfont, "White", 25, 200, 30)

    # Handle button clicks
    if leftbuttonrect.collidepoint(mousepos):
        if mousepress[0] and cooldown("button", 0.3):
            ControlIndex = (ControlIndex - 1) % len(Entity)  # Cycle to the previous index
    if rightbuttonrect.collidepoint(mousepos):
        if mousepress[0] and cooldown("button", 0.3):
            ControlIndex = (ControlIndex + 1) % len(Entity)  # Cycle to the next index

    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            states.pop()



#--------------------------------------------------------------------------------------------------#
def shop(screen):
    global buybutton
    vhs(screen)
    screen.blit(backbutton, backbuttonrect)
    flashlevel = checkstoreitem()
    moneydisplay = powerfont.render(f"Money: {str(Database.get_money())}", True, "White")
    screen.blit(moneydisplay, (50, 50))
    screen.blit(flashlevel, (800, 300))



    if (Database.get_money() < 100):
        buybutton = cantbuy
        screen.blit(buybutton, buybuttonrect)
    elif Database.get_inventory() >= 3:
        flashlevel = soldout
        buybutton = cantbuy
        screen.blit(buybutton, buybuttonrect)
    else:
        buybutton = canbuy
        screen.blit(buybutton, buybuttonrect)
        if buybuttonrect.collidepoint(mousepos):
            screen.blit(buybuttonp, buybuttonrect)
            if mousepress[0] and cooldown("buybutton",1):
                Database.change_money(-100)
                Database.change_flashlightlevel(1)

    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0] and cooldown("button",0.3):
            states.pop()

def generate_six_digit_code():
    global current_user
    if current_user and Database.get_stars() >= 5:
        return str(random.randint(100000, 999999))
    else:
        print("Access denied: Must be logged in and have 5 stars.")
        return None
    

def checkstoreitem():
    global flashlevel
    inventory_level = Database.get_inventory()
    if inventory_level == 0:
        flashlevel = bat1
    elif inventory_level == 1:
        flashlevel = bat2
    elif inventory_level == 2:
        flashlevel = bat3
    elif inventory_level == 3:
        flashlevel = soldout
    return flashlevel
    
# Options
def options(screen):
    global mousepos, mousepress, current_user, generated_code

    vhs(screen)
    screen.blit(loginbutton, loginbuttonrect)
    if loginbuttonrect.collidepoint(mousepos):
        screen.blit(loginbuttonp, loginbuttonrect)
        if mousepress[0]and cooldown("button",0.3):
            states.append(login)
    
    if generated_code is None:
        generated_code = generate_six_digit_code()

    if generated_code:
        entry_surface = powerfont.render(generated_code, True, "White")
        screen.blit(entry_surface, (1000, 100))  # Display the generated code

    screen.blit(logoutbutton, logoutbuttonrect)
    screen.blit(leaderboardbutton, leaderboardbuttonrect)
    screen.blit(backbutton, (600, 850))

    # Display the currently logged-in user
    if current_user:
        logged_in_text = powerfont.render(f"Logged in as: {current_user}", True, "White")
        screen.blit(logged_in_text, (300, 200))  
    else:
        logged_in_text = powerfont.render("Not logged in", True, "White")
        screen.blit(logged_in_text, (300, 200)) 

    # Handle logout button click
    if logoutbuttonrect.collidepoint(mousepos):
        screen.blit(logoutbuttonp, logoutbuttonrect)
        if mousepress[0] and current_user and cooldown("button",0.3):  # Only log out if a user is logged in
            Database.logout_user()
            current_user = None  # Reset the current user
            print("Logged out successfully.")
        elif mousepress[0] and not current_user and cooldown("button",0.3):
            print("No user is currently logged in.")

    # Handle back button click
    if optionsbackbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, (600, 850))
        if mousepress[0] and cooldown("button",0.3):
            states.pop()

    # Handle leaderboard button click
    if leaderboardbuttonrect.collidepoint(mousepos):
        screen.blit(leaderboardbuttonp, leaderboardbuttonrect)
        if mousepress[0] and cooldown("button",0.3):
            states.append(leaderboard)  # Switch to the leaderboard state

def leaderboard(screen):
    global mousepos, mousepress, leaderboard_data  

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display the leaderboard title
    title = powerfont.render("Leaderboard", True, "White")
    screen.blit(title, (600, 100))

    # Fetch the leaderboard data from the database
    leaderboard_data = Database.get_leaderboard(limit=10)  # Default to high scores leaderboard

    # Display each entry in the leaderboard
    y_offset = 200
    for rank, (username, score, money) in enumerate(leaderboard_data, start=1):
        entry_text = f"{rank}. {username}: {score} ${money}"
        entry_surface = powerfont.render(entry_text, True, "White")
        screen.blit(entry_surface, (600, y_offset))
        y_offset += 50  # Move down for the next entry

    # Display the back button
    screen.blit(backbutton, (600, 850))
    if optionsbackbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, (600, 850))
        if mousepress[0] and cooldown("button", 0.3):
            states.pop()  # Go back to the previous state (options)


def login(screen):
    global usernameinput, passwordinput, current_user

    screen.blit(logingui, (0, 0))
    screen.blit(backbutton, backbuttonrect)
    screen.blit(loginbutton, loginscreenbuttonrect)
    screen.blit(registerbutton, registerbuttonrect)

    # Display username and password fields
    usernameinput.display(usernamerect)
    passwordinput.display(passwordrect)

    # Handle focus switching
    if mousepress[0]:  # Check for mouse click
        if usernamerect.collidepoint(mousepos):  # Clicked on username field
            usernameinput.focus = True
            passwordinput.focus = False
        elif passwordrect.collidepoint(mousepos):  # Clicked on password field
            usernameinput.focus = False
            passwordinput.focus = True
        else:  # Clicked outside both fields
            usernameinput.focus = False
            passwordinput.focus = False

    # Handle back button
    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0] and cooldown("button", 0.3):
            states.pop()

    # Handle login button click (exclusively for logging in)
    if loginscreenbuttonrect.collidepoint(mousepos):
        screen.blit(loginbuttonp, loginscreenbuttonrect)
        if mousepress[0]:
            username = usernameinput.get_word()
            password = passwordinput.get_word()
            if Database.login_user(username, password):
                current_user = username  # Set the current user
                print(f"Logged in as {current_user}.")
                states.pop()  # Return to the previous state
            else:
                print("Invalid username or password.")

    # Handle register button click (exclusively for registering)
    if registerbuttonrect.collidepoint(mousepos):
        screen.blit(registerbuttonp, registerbuttonrect)
        if mousepress[0]:
            username = usernameinput.get_word()
            password = passwordinput.get_word()
            if Database.add_user(username, password):  # Attempt to register the user
                print(f"User {username} registered successfully.")
                # Automatically log in the newly registered user
                if Database.login_user(username, password):
                    current_user = username
                    print(f"Logged in as {current_user}.")
                    states.pop()  # Return to the previous state
            else:
                print("Registration failed. Username may already exist.")

def calculate_final_score():
    global final_score, power
    final_score = 0
    for enemy in enemygroup:
        final_score += enemy.difficulty * 10 + (power / 400)  # Each difficulty point counts as 10 points
    print(f"Final Score: {final_score}")

def update_highscore_if_needed():
    global current_user, final_score
    if current_user:
        current_highscore = Database.get_highscore(current_user)
        if final_score > current_highscore:
            Database.update_highscore(current_user, final_score)
            print(f"New high score: {final_score}")
        else:
            print(f"Current high score: {current_highscore} (Final score: {final_score})")
#==================================================================================================#

# Custom Enemies
cobybutton = CustomEnemy("Coby", 0, pygame.image.load("Data/States/Custom/Coby.png"), 530, 250)
customenemygroup.add(cobybutton)
codybutton = CustomEnemy("Cody", 0, pygame.image.load("Data/States/Custom/Cody.png"), 530, 510)
customenemygroup.add(codybutton)
chavobutton = CustomEnemy("Cedrick", 0, pygame.image.load("Data/States/Custom/Cedrick.png"), 1010, 510)
customenemygroup.add(chavobutton)
cedrickbutton = CustomEnemy("Chavo", 0, pygame.image.load("Data/States/Custom/Chavo.png"), 770, 250)
customenemygroup.add(cedrickbutton)
frederickbutton = (CustomEnemy("Frederick", 0, pygame.image.load("Data/States/Custom/Frederick.png"), 1010, 250))
customenemygroup.add(frederickbutton)
fredderickbutton = (CustomEnemy("FredDerick", 0, pygame.image.load("Data/States/Custom/Fred_Derrick.png"), 770, 510))
customenemygroup.add(fredderickbutton)


#==================================================================================================#
#Jumpscare loader
def jumpscareload(Name):
    jumpscarelist = []
    for i in os.listdir(f"./Data/Characters/{Name}/Jumpscare"):
        jumpscarelist.append(pygame.transform.scale(pygame.image.load(f"./Data/Characters/{Name}/Jumpscare/{i}").convert_alpha(),(1920, 1080)))
    return jumpscarelist


#Real Enemies

class Coby(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/Coby/CobyRest.png")
        self.hall = pygame.image.load("Data/Characters/Coby/CobyHall.png")
        self.wall = pygame.image.load("Data/Characters/Coby/CobyWall.png")
        self.office = imgimport("Data/Characters/Coby/CobyIn.png", (200, 200))
        self.jumpscare = jumpscareload("Coby")
        self.image = self.rest
        self.pathing = [3, 2 , 1, 0]
        self.imagearray = [self.rest, self.hall, self.wall, self.office]
        self.ticktime = 2
        self.flashlight = (-1700, -500)
        self.screenpos = (400, 400)

    def tick(self):
        global jumpscaretimer
        if self.pos == 0:
            if dlclosed:
                self.ticktime = 0.5
            elif not dlclosed:
                self.flashlight_sight()
        if cooldown(self.name, self.ticktime):
            if self.difficulty > random.randint(0, 20):
                self.move()

    def move(self):
        global inplay, power
        if self.pos == 0:
            if dlclosed:
                self.ticktime = 2
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
        self.jumpscare = jumpscareload("Cody")
        self.image = self.rest
        self.pathing = [3, 4 , 5, 0]
        self.imagearray = [self.rest, self.hall, self.wall, self.office]
        self.ticktime = 2
        self.flashlight = (-230, -500)
        self.screenpositon = (800, 400)
    
    def tick(self):
            global jumpscaretimer
            if self.pos == 0:
                if drclosed:
                    self.ticktime = 0.5
                elif not drclosed:
                    self.ticktime = 2
                    self.flashlight_sight()
            if cooldown(self.name, self.ticktime):
                if self.difficulty > random.randint(0, 20):
                    self.move()

    def move(self):
        global inplay
        if self.pos == 0:
            if drclosed:
                self.ticktime = 2
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
        self.jumpscare = jumpscareload("Cedrick")
        self.image = self.rest
        self.pathing = [3, 6, 0]
        self.imagearray = [self.rest, self.hall, self.office]
        self.ticktime = 2
        self.flashlight = (-1000, -600)
        self.screenpositon = (200, 400)
        self.activated = False
        self.flashlight_time = 0
        self.flashed = False
    def move(self):
        global inplay
        if self.pos == 6:
            self.activated = True
            super().move()
        elif self.pos == 0:
            if not self.activated:
                self.pos = 3
                self.image = self.rest
            if self.activated and not self.flashed:
                self.cankill = True
        else:
            super().move()
    def flashlight_sight(self):
        if flashlightpos == self.flashlight and flashlighton:
            self.flashlight_time += 1
            self.flashed = True
            self.ticktime = 0.5
        else:
            self.flashed = False
            self.ticktime = 2
        if self.flashlight_time >= 200:
            self.activated = False
            self.flashlight_time = 0
        super().flashlight_sight()
    def positionswitch(self):
        if self.pos != 0:
            self.screenpos = (800, 400)
        else:
            self.screenpos = (1000, 400)

class Chavo(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/Chavo/ChavoRest.png")
        self.hall = pygame.image.load("Data/Characters/Chavo/ChavoHall.png")
        self.wall = pygame.image.load("Data/Characters/Chavo/ChavoWall.png")
        self.right = pygame.image.load("Data/Characters/Chavo/ChavoRight.png")
        self.jumpscare = jumpscareload("Chavo")
        self.image = self.rest
        self.pathing = [3, 7, 8, 4]
        self.imagearray = [self.rest, self.hall, self.wall, self.right]
        self.ticktime = 3
        self.flashlight = (-1700, -500)
        self.screenpos = (400, 400)

    def move(self):
        global inplay, incameras
        if self.pos == 4:
            if not incameras:
                if drclosed:
                    self.pos = 3
                    self.image = self.rest
                if not drclosed:
                    self.cankill = True
        elif not incameras or hacked:
            super().move()
    
    def positionswitch(self):
        if self.pos != 4:
            self.screenpos = (400, 400)
        else:
            self.screenpos = (10, 400)

class Frederick(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/Frederick/FrederickRest.png")
        self.hack = imgimport("Data/Characters/Frederick/FrederickHack.png", (1920, 1080))
        self.revealed = imgimport("Data/Characters/Frederick/FrederickRevealed.png", (1920, 1080))
        self.jumpscare = jumpscareload("Frederick")
        self.image = self.rest
        self.imagearray = [self.rest, self.hack, self.revealed]
        self.ticktime = 5
        self.screenpos = (400, 400)
        self.tries = 2
        self.cankill = False
        self.hack_pos = 0
    
    def move(self):
        global cameraposarray,hacked,hack_pos
        hacked = True
        if hacked:
            shuffledcameras = []
            for i in range(0,8):
                shuffledcameras.append(self.hack)
            self.hack_pos = random.randint(0,7)
            shuffledcameras[self.hack_pos] = self.revealed
            cameraposarray[1:] = shuffledcameras
    def camera_click(self):
        global cameraposarray,hacked
        if self.hack_pos + 1 == camerapos and mousepress[0] and hacked and incameras:
            cameraposarray = [0, lwall, lhall, coop, rhall, rwall, fhall, uhall, uwall]
            hacked = False
        elif mousepress[0] and hacked and incameras and cooldown("Wrong_Hack",0.3):
            self.tries -= 1
        if self.tries <= 0:
            hacked = False
            self.cankill = True

    def update(self):
        self.camera_click()
        self.display()
        self.tick()
        self.positionswitch()
        self.killplayer()
        
class FredDerick(Enemy):
    def __init__(self, name, difficulty):
        super().__init__(name, difficulty)
        self.rest = pygame.image.load("Data/Characters/FredDerick/FredDerickRest.png")
        self.hall = pygame.image.load("Data/Characters/FredDerick/FredDerickHall.png")
        self.wall = pygame.image.load("Data/Characters/FredDerick/FredDerickWall.png")
        self.jumpscare = jumpscareload("FredDerick")
        self.image = self.rest
        self.imagearray = [self.wall, self.hall, self.rest]
        self.chance = 2
        if self.difficulty == 0:
            self.ticktime = 1000
        elif self.difficulty == 10:
            self.ticktime = 4
        else:
            self.ticktime = (15 - self.difficulty)
        self.flashlight = (-1700, -500)
        self.screenpos = (400, 400)
    def tick(self):
        global jumpscaretimer, tree
        if self.pos == 0:
            self.flashlight_sight()
        if cooldown(self.name, self.ticktime) and not inback:
            if len(tree.connections) != 0:
                tree.connections.pop()
            if len(tree.connections) == 0:
                if self.chance != 0:
                    tree.connect_nodes()
                    self.chance -= 1
                else:
                    self.cankill = True
    def display(self):
        global inback
        if inback:
            screen.blit(self.imagearray[self.chance], self.screenpos)
    def move(self):
        pass

#==================================================================================================#
 # Ensure one of each color per side

class Node:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.connected = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
        pygame.draw.circle(screen, "black", (self.x, self.y), 10, 2)  # Outline

class Tree:
    def __init__(self):
        self.colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "white", "brown"]
        self.left_nodes = [Node(random.randint(400, 700), random.randint(400, 600), self.colors[i]) for i in range(len(self.colors))]
        self.right_nodes = [Node(random.randint(1150, 1450), random.randint(400, 600), self.colors[i]) for i in range(len(self.colors))]  # Ensure one per side
        self.connections = set()
        self.selected_node = None
        self.connect_nodes()

    def connect_nodes(self):
            for left_node in self.left_nodes:
                for right_node in self.right_nodes:
                    if left_node.color == right_node.color:
                        self.connections.add((left_node, right_node))
    def draw_nodes(self, screen):
        for node in self.left_nodes + self.right_nodes:
            node.draw(screen)

    def draw_connections(self, screen):
        for (node1, node2) in self.connections:
            pygame.draw.line(screen, "brown", (node1.x, node1.y), (node2.x, node2.y), 5)
        
        if self.selected_node and mousepos:
            pygame.draw.line(screen, "brown", (self.selected_node.x, self.selected_node.y), mousepos, 2)

    def find_node(self, x, y):
        for node in self.left_nodes + self.right_nodes:
            if (node.x - 10 < x < node.x + 10) and (node.y - 10 < y < node.y + 10):
                return node
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            self.selected_node = self.find_node(x, y)
        elif event.type == pygame.MOUSEMOTION:
            mousepos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and self.selected_node:
            x, y = pygame.mouse.get_pos()
            target_node = self.find_node(x, y)
            
            # Ensure connection is valid
            if target_node and target_node != self.selected_node:
                if self.selected_node.color == target_node.color and (self.selected_node in self.left_nodes) != (target_node in self.left_nodes):
                    if (self.selected_node, target_node) not in self.connections or (target_node, self.selected_node) not in self.connections:
                        self.connections.add((self.selected_node, target_node))
            
            self.selected_node = None  # Reset selection
            mousepos = None  # Reset mouse position

tree = Tree()


def minigameevent(screen):
    tree.draw_nodes(screen)
    tree.draw_connections(screen)  
#==================================================================================================#
# Customscreen
def customscreen(screen):
    global final_score

    vhs(screen)
    screen.blit(customborders, (360, 90))
    screen.blit(backbutton, backbuttonrect)
    screen.blit(beginbutton, beginbuttonrect)
    customenemygroup.draw(screen)
    customenemygroup.update()
    if backbuttonrect.collidepoint(mousepos):
        screen.blit(backbuttonp, backbuttonrect)
        if mousepress[0] and cooldown("button",0.3):
            states.pop()
    if beginbuttonrect.collidepoint(mousepos):
        screen.blit(beginbuttonp, beginbuttonrect)
        if mousepress[0]:
            reset()
            enemygroup.add(Coby("Coby", cobybutton.returndifficulty()))
            enemygroup.add(Cody("Cody", codybutton.returndifficulty()))
            enemygroup.add(Cedrick("Cedrick", cedrickbutton.returndifficulty()))
            enemygroup.add(Chavo("Chavo", chavobutton.returndifficulty()))
            enemygroup.add(FredDerick("FredDerick", fredderickbutton.returndifficulty()))
            enemygroup.add(Frederick("Frederick", frederickbutton.returndifficulty()))
            calculate_final_score()  # Calculate the final score
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
hacked = False

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
    global inoffice, incameras, inback, flashlighton, flashlightpos, incameras, inback, power, rawtime, inplay, jumpscaretimer, hacked, tree, cameraposarray, powermultiplier
    jumpscaretimer = 0
    inoffice = True
    flashlighton = False
    incameras = False
    inback = False
    flashlightpos = (-1000, -600)
    incameras = False
    inback = False
    powermultiplier = (((Database.get_inventory()) / 5) + 1)
    power = 40000 * powermultiplier
    rawtime = int(time.time())
    inplay = True
    hacked = False
    enemygroup.empty()
    tree = Tree()
    cameraposarray = [0, lwall, lhall, coop, rhall, rwall, fhall, uhall, uwall]

# Game
def game(screen):
    global inoffice, flashlighton, flashlightpos, incameras, inback, power, rawtime, hacked
    power -= 2
    powerdisplay = powerfont.render(str(power//400)+"%", True, "White")
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
        if not flashlighton and not dying:
            screen.blit(dark, (0, 0))
        if flashlighton and not dying:
            screen.blit(flashlight, flashlightpos)
            power -= 5
    if (elapsed_time // 60) == 6:
        states.append(win)
    if power <= 0:
        states.append(lose)
    can_rain = camerapos != 6 and not hacked
    if incameras:
        screen.fill((0, 0, 0))
        numcam()
        screen.blit(cameraposarray[camerapos], (0, 0))
        enemygroup.update()
        if can_rain:
            rain(screen)
        screen.blit(dark, (0, 0))
        if keys[pygame.K_c] and cooldown("cameras", 0.2):
            inoffice = True
            incameras = False
    if inback:
        screen.fill((0, 0, 0))
        screen.blit(back, (0, 0))
        enemygroup.update()
        tree.draw_nodes(screen)
        tree.draw_connections(screen)  
        screen.blit(dark, (0, 0))
        if keys[pygame.K_x] and cooldown("back", 0.2):
            inoffice = True
            inback = False
    if not dying:
        screen.blit(powerdisplay,(0,1000))
        screen.blit(TimeDisplay, (0,0))
    

# Win Screen
def win(screen):
    global final_score, current_user, customgame

    screen.fill((0, 0, 0))
    vhs(screen)
    win = powerfont.render("You Win (Press space to return to menu)", True, "White")
    screen.blit(win, center)

    # Update the high score if needed
    update_highscore_if_needed()

    # Add the final score to the user's money


    if keys[pygame.K_SPACE]:
        if current_user:
            Database.change_money(final_score)
            print(f"Added {final_score} to {current_user}'s money.")

            # Increase stars by 1 (capped at 5) if it's not a custom game
            if not customgame:
                current_stars = Database.get_stars()
                if current_stars < 5:
                    Database.change_stars(1)
                    print(f"Added 1 star to {current_user}'s profile. Current stars: {current_stars + 1}")
                else:
                    print(f"{current_user} already has the maximum number of stars (5).")
            else:
                print("No stars awarded for custom games.")
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
    # Debug: Press K to instantly win
    if keys[pygame.K_k] and cooldown("debug", 2):
        debug_win()

    if current_user:
        if mousepress[2]:
            Database.change_money(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if current_user != None:
                Database.logout_user()
                current_user = None  # Reset the current user
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Handle keypresses only if the login screen is active
            if states[-1] == login:
                if usernameinput.focus:
                    usernameinput.add(event.key)
                elif passwordinput.focus:
                    passwordinput.add(event.key)
            if event.key == pygame.K_ESCAPE:
                if current_user != None:
                    Database.logout_user()
                    current_user = None  # Reset the current user
                pygame.quit()
                exit()
        else:
            tree.handle_event(event)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Call the current state function
    states[-1](screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    time2dp = round(time.time(),2)