import pygame, random

pygame.init()

Jede = True
Scena = "menu"

Okno_Sirka = 800
Okno_vyska = 600
Okno = pygame.display.set_mode((Okno_Sirka, Okno_vyska))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("Raketka.png"))
Pozadi_Hry = pygame.image.load("Pozadi1.png").convert()
Pozadi_Hry = pygame.transform.scale(Pozadi_Hry, (Okno_Sirka, Okno_vyska))

StylNadpisu = pygame.font.Font("freesansbold.ttf", 75)
Nadpis = StylNadpisu.render("SPACE INVADERS", True, (0, 255, 255))

Start_Button = pygame.Rect(250, 250, 300, 100)
Styl = pygame.font.Font("freesansbold.ttf", 50)
Start_Text = Styl.render("START", True, (0, 0, 0))

Zpet_Button = pygame.Rect(Okno_Sirka / 2 - 20, 2, 20, 20)
Zpet = pygame.image.load("Zpet.png").convert_alpha()
Zpet = pygame.transform.scale(Zpet, (20, 20))

Anulace = pygame.Rect(250, 360, 300, 50)
Anulace_Styl = pygame.font.Font("freesansbold.ttf", 30)
Anulace_Text = Anulace_Styl.render("VYNULOVAT", True, (0, 0, 0))
Vynulováno = Anulace_Styl.render("VYNULOVÁNO!", True, (255, 255, 255))
a = 0

FPS = 60
Hodiny = pygame.time.Clock()

Skore = 0
SkoreX = Okno_Sirka - 150
SkoreY = 0
SkoreStyl = pygame.font.Font("freesansbold.ttf", 32)

ij = 0
def HudbaVMenu():
    global ij
    MenuHudba = "MenuBackgroundSound.mp3"
    pygame.mixer.music.load(MenuHudba)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    ij += 1

j = 0
def HudbaVeHre():
    global j
    GameBackgroundSound = "GameBackgroundSound.mp3"
    pygame.mixer.music.load(GameBackgroundSound)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    j += 1

def HudbaProhry():
    hudba = pygame.mixer.Sound("Prohra.mp3")
    hudba.set_volume(0.1)
    pygame.mixer.music.stop()
    hudba.play()

# Hrac/raketka
Raketka = pygame.image.load("Raketka.png").convert_alpha()
Raketka = pygame.transform.scale(Raketka, (50, 50))
RaketkaX = ((Okno_Sirka / 2) - 50)
RaketkaY = (Okno_vyska - 60)
RaketkaRychlost = 4

# strela
Strela = pygame.image.load("Strela.png").convert_alpha()
Strela = pygame.transform.scale(Strela, (20, 20))
StrelaX = Okno_Sirka / 2 - 35
StrelaY = Okno_vyska - 75
StrelaRychlost = 4
StatusStrely = "pripravena"
ZvukVystrelu = pygame.mixer.Sound("Vystrel.wav")

def vystrel(x, y):
    global StatusStrely
    StatusStrely = "vystrelila"
    Okno.blit(Strela, (x, y))

nepritel = pygame.image.load("Nepritel.png").convert_alpha()
nepritel = pygame.transform.scale(nepritel, (50, 50))
nepratele = []

class Nepritel(pygame.Rect):
    def __init__(a):
        a.x = random.randint(51, Okno_Sirka - 51)
        a.y = 50
        a.width = 50
        a.height = 50
        a.rychlost = 4
        a.zmena = 50
        a.z = random.randint(0, 1)
        if a.z == 0:
            a.smer = "doprava"
        else:
            a.smer = "doleva"

    def pohyb(a):
        if a.smer == "doprava":
            a.x += a.rychlost
        elif a.smer == "doleva":
            a.x -= a.rychlost
        if a.x <= 0:
            a.smer = "doprava"
            a.y += a.zmena
        elif a.x >= (Okno_Sirka - a.width):
            a.smer = "doleva"
            a.y += a.zmena

    def tezsi(a):
        if Skore % 15 == 0 and Skore > 0:
            a.rychlost += 3

    def zasah(a):
        global Skore, StrelaY, StrelaRychlost, StatusStrely, vytvorit
        strelaRect = pygame.Rect(StrelaX, StrelaY, 25, 25)
        vybuch = pygame.mixer.Sound("explosion.wav")
        if a.colliderect(strelaRect):
            vybuch.play()
            Skore += 1
            a.x = random.randint(0, Okno_Sirka - 5)
            a.y = 50
            StrelaY = Okno_vyska - 60
            StatusStrely = "pripravena"
            vytvorit = True

vytvorit = True
def novy():
    global nepratele, vytvorit
    if Skore == 0 or Skore % 10 == 0:
        if vytvorit:
            nepratele.append(Nepritel())
            vytvorit = False

def vykreslit():
    for i in nepratele:
        Okno.blit(nepritel, i)

Prohrals = False
ZnovuPos = 250
Znovu_Button = pygame.Rect(ZnovuPos, ZnovuPos, 300, 100)
Prohra_Text = Styl.render("ZNOVU!", True, (0, 0, 0))
def Prohra():
    global Prohrals, NejlepsiSkore
    for i in nepratele:
        if i.y >= (Okno_vyska - 100):
            Prohrals = True
            i.rychlost = 0
            i.zmena = 2
            HudbaProhry()
    if Prohrals:
        pygame.draw.rect(Okno, (255, 255, 255), Znovu_Button, 0, 30)
        Okno.blit(Prohra_Text, (305, 275))
    if Skore > NejlepsiSkore and Prohrals:
        NejlepsiSkore = Skore
        f = open("NejSkore.txt", "w")
        f.write(str(Skore))
        f.close()

def Vynulovat():
    global a
    a = 1
    f = open("NejSkore.txt", "w")
    f.write("0")
    f.close()

NejlepsiSkore = 0
while Jede:
    Hodiny.tick(FPS)
    Okno.fill((0, 0, 0))
    Klavesa = pygame.key.get_pressed()

    if Scena == "menu":
        pygame.draw.rect(Okno, (170, 0, 255), Start_Button, 0, 30)
        pygame.draw.rect(Okno, (170, 0, 255), Anulace, 0, 30)
        Okno.blit(Start_Text, (325, 275))
        Okno.blit(Nadpis, (75, 100))
        Okno.blit(Anulace_Text, (310, 370))

        if ij == 0:
            HudbaVMenu()

        if a == 1:
            Okno.blit(Vynulováno, (290, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Jede = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Start_Button.collidepoint(mouse_pos):
                    Scena = "hra"
                    a = 0
                    pygame.mixer.music.stop()
                    HudbaVeHre()
                    f = open("NejSkore.txt", "r")
                    NejlepsiSkore = int(f.read())
                if Anulace.collidepoint(mouse_pos):
                    Vynulovat()

    elif Scena == "hra":
        Okno.blit(Pozadi_Hry, (0, 0))
        Okno.blit(Raketka, (RaketkaX, RaketkaY))
        pygame.draw.line(Okno, (255, 255, 255), (0, Okno_vyska - 100), (Okno_Sirka, Okno_vyska - 100), 2)
        pygame.draw.rect(Okno, (255, 255, 255), Zpet_Button, 0, 3)
        Okno.blit(Zpet, (Okno_Sirka / 2 - 20, 1))

        skore = SkoreStyl.render("Skóre: " + str(Skore), True, (255, 255, 255))
        Okno.blit(skore, (SkoreX, SkoreY))
        Nej_Text = SkoreStyl.render("Nejlepší skóre: " + str(NejlepsiSkore), True, (255, 255, 255))
        Okno.blit(Nej_Text, (10, 2))

        if j == 0:
            HudbaVeHre()

        novy()
        vykreslit()
        for i in nepratele:
            i.pohyb()
            i.zasah()
            i.tezsi()
        Prohra()

        if Klavesa[pygame.K_LEFT] and RaketkaX >= 0:
            RaketkaX -= RaketkaRychlost
        if Klavesa[pygame.K_RIGHT] and RaketkaX <= (Okno_Sirka - 50):
            RaketkaX += RaketkaRychlost
        if Klavesa[pygame.K_SPACE]:
            if StatusStrely == "pripravena":
                ZvukVystrelu.play()
                ZvukVystrelu.set_volume(0.1)
                StrelaX = RaketkaX
                vystrel(StrelaX + 15, StrelaY)
        if Klavesa[pygame.K_ESCAPE]:
            pygame.mixer.music.stop()
            Scena = "menu"
            HudbaVMenu()

        if StrelaY <= 0 - 20:
            StrelaY = Okno_vyska - 75
            StatusStrely = "pripravena"
        if StatusStrely == "vystrelila":
            vystrel(StrelaX + 15, StrelaY)
            StrelaY -= StrelaRychlost

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Jede = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Zpet_Button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    Scena = "menu"
                    HudbaVMenu()
                if Znovu_Button.collidepoint(mouse_pos) and Prohrals:
                    Skore = 0
                    HudbaVeHre()
                    nepratele = []
                    Prohrals = False
                    vytvorit = True
                    RaketkaX = (Okno_Sirka / 2) - 50


    pygame.display.flip()