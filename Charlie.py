import pygame

pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Charlie's Farm")
clock = pygame.time.Clock()
PowerFont = pygame.font.Font(None, 50)
center = (600,450)
Transparent = (0, 0, 0, 0)

#GAME STATES
poosigma = True
Mainscreen = True
Options = False
Game = False
Over = False
Custom = False
Canpress = -1
black = pygame.image.load("v10/Data/Map/black.png")

#INGAME STATES
Main = True
Cams = False
Backdoor = False
def Reset(): #resets values to default everytime player starts a new agme
    global Power, FlashlightPOS, FX, FY, PowerDrain
    Power = 20000
    FlashlightPOS = 1
    FX = -230
    FY = -400
    PowerDrain = 1

#Mechanics
Dark = pygame.image.load("Data/Mechanics/Dark.png")
Flashlight = pygame.image.load("Data/Mechanics/flashlight.png")
Power = 0
FX = -800
FY = -400

#COOLDOWNS
Xcanpress = True
BackCD = [-1]
Ccanpress = True
CamCD = [-1]
def Cooldown(Pressable, CD, MAX): #cooldown function to set a CD to be MAX seconds long
    global Xcanpress, Ccanpress
    if CD[0] == -1:
        CD[0] = 0
        print("signa")
    if CD[0] >= 0:
        CD[0] += 1
        print("CD")
        if CD[0] >= MAX:
            CD[0] = -1
            print("CD READY")
            if Pressable == 1:
                Xcanpress = True
            elif Pressable == 2:
                Ccanpress = True
#Camera Effect
CHS0 = pygame.image.load("Data/Map/CameraEffect/frame_0_delay-0.05s.png")
CHS1 = pygame.image.load("Data/Map/CameraEffect/frame_1_delay-0.05s.png")
CHS2 = pygame.image.load("Data/Map/CameraEffect/frame_2_delay-0.05s.png")
CHS3 = pygame.image.load("Data/Map/CameraEffect/frame_3_delay-0.05s.png")
CHS4 = pygame.image.load("Data/Map/CameraEffect/frame_4_delay-0.05s.png")
CHS5 = pygame.image.load("Data/Map/CameraEffect/frame_5_delay-0.05s.png")
CHS6 = pygame.image.load("Data/Map/CameraEffect/frame_6_delay-0.05s.png")
CHS7 = pygame.image.load("Data/Map/CameraEffect/frame_7_delay-0.05s.png")

CHSINDEX = 0
CHS = [CHS0, CHS1, CHS2, CHS3, CHS4, CHS5, CHS6, CHS7]
def CHSEFFECT():
    global CHSINDEX
    for i in range (0,2):
        CHS[CHSINDEX] = pygame.transform.scale(CHS[CHSINDEX], (1920, 1080))
        screen.blit(CHS[CHSINDEX], (0,0))
        CHSINDEX += 1
        if CHSINDEX >= 7:
            CHSINDEX = 0
#VHS EFFECT
VHS0 = pygame.image.load("Data/Mainscreen/VHS/0.png")
VHS1 = pygame.image.load("Data/Mainscreen/VHS/1.png")
VHS2 = pygame.image.load("Data/Mainscreen/VHS/2.png")
VHS3 = pygame.image.load("Data/Mainscreen/VHS/3.png")
VHS4 = pygame.image.load("Data/Mainscreen/VHS/4.png")
VHS5 = pygame.image.load("Data/Mainscreen/VHS/5.png")
VHSINDEX = 0
VHS = [VHS0, VHS1, VHS2, VHS3, VHS4, VHS5]
def VHSEFFECT():
    global VHSINDEX
    for i in range (0,5):
        screen.blit(VHS[VHSINDEX], (0,0))
        VHSINDEX += 1
        if VHSINDEX >= 6:
            VHSINDEX = 0
        


#Mainscreen
Playbutton = pygame.image.load("Data/Mainscreen/Playbutton.png")
PlaybuttonP = pygame.image.load("Data/Mainscreen/PlaybuttonP.png")
PlaybuttonRect = Playbutton.get_rect(center = (300,600))
Title = PowerFont.render("Charlie's Farm", True, "White")

Quitbutton = pygame.image.load("Data/Mainscreen/Quitbutton.png")
QuitbuttonP = pygame.image.load("Data/Mainscreen/QuitbuttonP.png")
QuitbuttonRect = Quitbutton.get_rect(center = (300, 900))

Optionsbutton = pygame.image.load("Data/Mainscreen/Optionsbutton.png")
OptionsbuttonP = pygame.image.load("Data/Mainscreen/OptionsbuttonP.png")
OptionsbuttonRect = Optionsbutton.get_rect(center = (375, 750))

CharliePFP = pygame.image.load("Data/Mainscreen/Charlie.png")

#CustomScreen
Customborders = pygame.image.load("Data/Custom/CustomBorders.png")
Customborders = pygame.transform.scale(Customborders,(1200,900))

Backbutton = pygame.image.load("Data/Custom/Backbutton.png")
BackbuttonP = pygame.image.load("Data/Custom/BackbuttonP.png")
BackbuttonRect = Backbutton.get_rect(center = (200, 850))

ArrowR = pygame.image.load("Data/Custom/ArrowR.png")
ArrowR = pygame.transform.scale(ArrowR, (30, 30))
ArrowL = pygame.image.load("Data/Custom/ArrowL.png")
ArrowL = pygame.transform.scale(ArrowL, (30, 30))

BeginButton = pygame.image.load("Data/Custom/Begin.png")
BeginButtonR = pygame.image.load("Data/Custom/BeginR.png")
BeginButtonP = pygame.image.load("Data/Custom/BeginP.png")
BeginButtonRect = BeginButton.get_rect(center = (1500, 850))

#GameOver Screen
OverScreen = pygame.image.load("Data/GameOver/OverScreen.png")
OverScreen = pygame.transform.scale(OverScreen, (1920, 1080))

Menubutton = pygame.image.load("Data/GameOver/MenuButton.png")
MenubuttonP = pygame.image.load("Data/GameOver/MenuButtonP.png")
MenubuttonRect = Menubutton.get_rect(center = (960, 700))

#GAME MAP default: 480 x 270, DOOR = 104 x 124
def map_import(map):
    newmap = pygame.image.load(map)
    newmap = pygame.transform.scale(newmap,(1920,1080))
    return newmap
Office = map_import("Data/Map/Office.png")
Back = map_import("Data/Map/Back.png")
Dark = map_import("Data/Mechanics/Dark.png")
Coop = map_import("Data/Map/Coop.png")
LWall = map_import("Data/Map/LeftWall.png")
LHall = map_import("Data/Map/LeftHall.png")
RWall = map_import("Data/Map/RightWall.png")
RHall = map_import("Data/Map/RightHall.png")
UWall = map_import("Data/map/UpWall.png")
UHall = map_import("Data/Map/UpHall.png")

#CustomCharacters
CharacterBar1 = PowerFont.render(" Chavo                Cody                 Coby", True, "White")
CharacterBar2 = PowerFont.render(" Frederick           Cedrick         Fred-Derrick", True, "White")

#Character iamges
CChavoPFP = pygame.image.load("Data/Custom/Chavo.png")
CChavoPFP = pygame.transform.scale(CChavoPFP, (180, 160))
CCodyPFP = pygame.image.load("Data/Custom/Cody.png")
CCodyPFP = pygame.transform.scale(CCodyPFP, (180,160))
CCobyPFP = pygame.image.load("Data/Custom/Coby.png")
CCobyPFP = pygame.transform.scale(CCobyPFP, (180,160))
CFrederickPFP = pygame.image.load("Data/Custom/Frederick.png")
CFrederickPFP = pygame.transform.scale(CFrederickPFP, (180,160))
CCedrickPFP = pygame.image.load("Data/Char/Mainscreen.png")
CCedrickPFP = pygame.transform.scale(CCedrickPFP, (180, 160))
CFred_DerrickPFP = pygame.image.load("Data/Custom/Fred_Derrick.png")
CFred_DerrickPFP = pygame.transform.scale(CFred_DerrickPFP, (180,160))

#Custom Character Creator
class CustomChar():
    def __init__(self,diff, pfp, LR, RR):
        self.diff = diff
        self.pfp = pfp
        self.LR = LR
        self.RR = RR
CChavo = CustomChar(0, CChavoPFP, ArrowL.get_rect(center = (120, 280)),ArrowR.get_rect(center = (220, 280)))
CCody = CustomChar(0, CCodyPFP, ArrowL.get_rect(center = (360, 280)), ArrowR.get_rect(center = (460, 280)))
CCoby = CustomChar(0, CCobyPFP, ArrowL.get_rect(center = (600, 280)), ArrowR.get_rect(center = (700, 280)))
CFrederick = CustomChar(0, CFrederickPFP, ArrowL.get_rect(center = (120, 570)), ArrowR.get_rect(center = (220, 570)))
CCedrick = CustomChar(0, CCedrickPFP, ArrowL.get_rect(center = (360, 570)), ArrowR.get_rect(center = (460, 570)))
CFred_Derrick = CustomChar(0, CFred_DerrickPFP, ArrowL.get_rect(center = (600, 570)), ArrowR.get_rect(center = (700, 570)))

#Camera states
Changepos = 0
CameraPos = 0
CurrentCam = [LWall, LHall,RWall, RHall, UWall, UHall, Coop]
def NumCam():
    global CameraPos
    if keys[pygame.K_1]:
        CameraPos = 0
    if keys[pygame.K_2]:
        CameraPos = 1
    if keys[pygame.K_3]:
        CameraPos = 2
    if keys[pygame.K_4]:
        CameraPos = 3
    if keys[pygame.K_5]:
        CameraPos = 4
    if keys[pygame.K_6]:
        CameraPos = 5
    if keys[pygame.K_7]:
        CameraPos = 6
#Main
while True:
    mousepos = pygame.mouse.get_pos()
    mousepress = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    if mousepress[0] and Canpress == -1:
        Canpress = 0
    if Canpress != -1:
        Canpress += 1
    if Canpress >= 5:
        Canpress = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if Mainscreen:
        VHSEFFECT()
        screen.blit(Title,(200, 200))
        screen.blit(Playbutton, PlaybuttonRect)
        screen.blit(Quitbutton, QuitbuttonRect)
        screen.blit(Optionsbutton, OptionsbuttonRect)
        screen.blit(CharliePFP, (1200, 600))
        if PlaybuttonRect.collidepoint(mousepos):
            screen.blit(PlaybuttonP, PlaybuttonRect)
            if mousepress[0]:
                Custom = True
                Mainscreen = False
        if OptionsbuttonRect.collidepoint(mousepos):
            screen.blit(OptionsbuttonP, OptionsbuttonRect)
            if mousepress[0]:
                Options = True
                Mainscreen = False
        if QuitbuttonRect.collidepoint(mousepos):
            screen.blit(QuitbuttonP, QuitbuttonRect)
            if mousepress[0]:
                pygame.quit()
                exit()
    if Custom: #Custom
        CChavoText = PowerFont.render(str(CChavo.diff), True, "White")
        CFrederickText = PowerFont.render(str(CFrederick.diff), True, "White")
        CCodyText = PowerFont.render(str(CCody.diff), True, "White")
        CCobyText = PowerFont.render(str(CCoby.diff), True, "White")
        CCedrickText = PowerFont.render(str(CCedrick.diff), True, "White")
        CFred_DerrickText = PowerFont.render(str(CFred_Derrick.diff), True, "White")
        VHSEFFECT()
        screen.blit(Customborders,(0,0))
        screen.blit(Backbutton, BackbuttonRect)
        screen.blit(BeginButton, BeginButtonRect)
        screen.blit(CharacterBar1,(100, 25))
        screen.blit(CharacterBar2,(80, 520))
        screen.blit(CChavoText, (160, 265))
        screen.blit(CChavo.pfp, (80, 80))
        screen.blit(ArrowL, (CChavo.LR))
        screen.blit(ArrowR, (CChavo.RR))
        screen.blit(CFrederickText, (160, 555))
        screen.blit(CFrederickPFP, (80, 340))
        screen.blit(ArrowL, (CFrederick.LR))
        screen.blit(ArrowR, (CFrederick.RR))
        screen.blit(CCodyText, (400, 265))
        screen.blit(CCodyPFP, (320,80))
        screen.blit(ArrowL, (CCody.LR))
        screen.blit(ArrowR, (CCody.RR))
        screen.blit(CCobyText, (640, 265))
        screen.blit(CCobyPFP, (560, 80))
        screen.blit(ArrowL, (CCoby.LR))
        screen.blit(ArrowR, (CCoby.RR))
        screen.blit(CFred_DerrickText, (640, 555))
        screen.blit(CFred_DerrickPFP, (560, 340))
        screen.blit(ArrowL, (CFred_Derrick.LR))
        screen.blit(ArrowR, (CFred_Derrick.RR))
        screen.blit(CCedrickText, (400, 555))
        screen.blit(CCedrickPFP, (320, 340))
        screen.blit(ArrowL, (CCedrick.LR))
        screen.blit(ArrowR, (CCedrick.RR))
        if CChavo.diff >= 11: #Custom difficulty selection for each character
            CChavo.diff = 0
        if CChavo.diff <= -1:
            CChavo.diff = 10
        if CChavo.LR.collidepoint(mousepos):
            if mousepress[0] and CChavo.diff < 11 and CChavo.diff > -1 and Canpress == -1:
                CChavo.diff -= 1
        if CChavo.RR.collidepoint(mousepos):
            if mousepress[0] and CChavo.diff < 11 and CChavo.diff > -1 and Canpress == -1:
                CChavo.diff += 1
        if CFrederick.diff >= 11:
            CFrederick.diff = 0
        if CFrederick.diff <= -1:
            CFrederick.diff = 10
        if CFrederick.LR.collidepoint(mousepos):
            if mousepress[0] and CFrederick.diff < 11 and CFrederick.diff > -1 and Canpress == -1:
                CFrederick.diff -= 1
        if CFrederick.RR.collidepoint(mousepos):
            if mousepress[0] and CFrederick.diff < 11 and CFrederick.diff > -1 and Canpress == -1:
                CFrederick.diff += 1
        if CCody.diff >= 11:
            CCody.diff = 0
        if CCody.diff <= -1:
            CCody.diff = 10
        if CCody.LR.collidepoint(mousepos):
            if mousepress[0] and CCody.diff < 11 and CCody.diff > -1 and Canpress == -1:
                CCody.diff -= 1
        if CCody.RR.collidepoint(mousepos):
            if mousepress[0] and CCody.diff < 11 and CCody.diff > -1 and Canpress == -1:
                CCody.diff += 1
        if CCoby.diff >= 11:
            CCoby.diff = 0
        if CCoby.diff <= -1:
            CCoby.diff = 10
        if CCoby.LR.collidepoint(mousepos):
            if mousepress[0] and CCoby.diff < 11 and CCoby.diff > -1 and Canpress == -1:
                CCoby.diff -= 1
        if CCoby.RR.collidepoint(mousepos):
            if mousepress[0] and CCoby.diff < 11 and CCoby.diff > -1 and Canpress == -1:
                CCoby.diff += 1
        if CFred_Derrick.diff >= 11:
            CFred_Derrick.diff = 0
        if CFred_Derrick.diff <= -1:
            CFred_Derrick.diff = 10
        if CFred_Derrick.LR.collidepoint(mousepos):
            if mousepress[0] and CFred_Derrick.diff < 11 and CFred_Derrick.diff > -1 and Canpress == -1:
                CFred_Derrick.diff -= 1
        if CFred_Derrick.RR.collidepoint(mousepos):
            if mousepress[0] and CFred_Derrick.diff < 11 and CFred_Derrick.diff > -1 and Canpress == -1:
                CFred_Derrick.diff += 1
        if CCedrick.diff >= 11:
            CCedrick.diff = 0
        if CCedrick.diff <= -1:
            CCedrick.diff = 10
        if CCedrick.LR.collidepoint(mousepos):
            if mousepress[0] and CCedrick.diff < 11 and CCedrick.diff > -1 and Canpress == -1:
                CCedrick.diff -= 1
        if CCedrick.RR.collidepoint(mousepos):
            if mousepress[0] and CCedrick.diff < 11 and CCedrick.diff > -1 and Canpress == -1:
                CCedrick.diff += 1
        if BackbuttonRect.collidepoint(mousepos):
            screen.blit(BackbuttonP, BackbuttonRect)
            if mousepress[0]:
                Custom = False
                Mainscreen = True
        if BeginButtonRect.collidepoint(mousepos):
            screen.blit(BeginButtonP, BeginButtonRect)
            if mousepress[0]:
                Reset()
                Game = True
                Custom = False
    if Game: #when game is active // at any point in the game
        screen.blit(black, (0,0))
        Power -= 1
        if Xcanpress == False:
          Cooldown(1, BackCD, 10)
        if Ccanpress == False:
          Cooldown(2, CamCD, 10)
        if Main:
            screen.blit(Office, (0,0))
            screen.blit(Dark, (0,0))
            PowerDisplay = PowerFont.render(str(Power//200)+"%", True, "White")
            if keys[pygame.K_a] and FlashlightPOS != 0:
                FlashlightPOS = 0
            if keys[pygame.K_d] and FlashlightPOS != 2:
                FlashlightPOS = 2
            if keys[pygame.K_w] and FlashlightPOS != 3:
                FlashlightPOS = 3
            if keys[pygame.K_s] and FlashlightPOS != 1:
                FlashlightPOS = 1
            if FlashlightPOS == 0:
                FX = -1700
                FY = -500
            if FlashlightPOS == 1:
                FX = -1000
                FY = -600
            if FlashlightPOS == 2:
                FX = -230
                FY = -500
            if FlashlightPOS == 3:
                FX = -1400
                FY = -1000
            if PowerDrain != FlashlightPOS:
                Power = Power - 20
                PowerDrain = FlashlightPOS
            screen.blit(Flashlight, (FX,FY))
            screen.blit(PowerDisplay,(0,1000))
            if keys[pygame.K_x] and Xcanpress:
                Backdoor = True
                Main = False
                Xcanpress = False
                print("Here")
            if keys[pygame.K_c] and Ccanpress:
                Cams = True
                Main = False
                Ccanpress = False
        if Backdoor:
            screen.blit(black, (0,0))
            screen.blit(Back, (0,0))
            screen.blit(Dark, (0,0))
            if keys[pygame.K_x] and Xcanpress:
                Main = True
                Backdoor = False
                Xcanpress = False
                print("Test")
        if Power <= 0:
            Game = False
            Over = True
        if Power > 0:
            Over = False
        if Cams:
            Power -= 1
            screen.blit(black, (0,0))
            NumCam()
            screen.blit(CurrentCam[CameraPos], (0,0))
            CHSEFFECT()
            screen.blit(Dark,(0,0))
            
            if keys[pygame.K_c] and Ccanpress:
                Main = True
                Cams = False
                Ccanpress = False
    if Over:
        Cams = False
        Backdoor = False
        Main = True
        screen.blit(OverScreen, (0,0))
        screen.blit(Menubutton, (MenubuttonRect))
        if MenubuttonRect.collidepoint(mousepos):
            screen.blit(MenubuttonP, MenubuttonRect)
            if mousepress[0]:
                Mainscreen = True
                Over = False
    pygame.display.update()
    clock.tick(60)