#importing and initialising pygame
import pygame
import random
from random import randint
pygame.init()
#colours
colourRed = (255, 0, 0)
colourBlack = (0, 0, 0)
colourBlue = (0, 0, 255)
colourWhite = (255, 255, 255)
colourGreen = (0, 100, 0)
ballColour = (198, 237, 44)
#general variables
player1score = 0
player2score = 0
clock = pygame.time.Clock()
#setting up window
gameWindow = pygame.display.set_mode((700, 500))
#menu function
def pong_menu():
    #colours
    global colourRed
    global colourBlack
    global colourBlue
    global colourWhite
    global colourGreen
    global multi_ballColour
    #setting up window
    global gameWindow
    pygame.display.set_caption("Pong")
    #add description
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #menu background colour
        gameWindow.fill(colourGreen)
        #menu text
        font = pygame.font.Font(None, 115)
        text = font.render("Pong", 1, colourWhite)
        gameWindow.blit(text, (15, 10))
        #button function
        def button(colour, x, y, width, height, action):
            #adds mouse position checker and click command
            mousePosition = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            #draws button
            pygame.draw.rect(gameWindow, colour, (x, y, width, height))
            #button functionality
            if x + width > mousePosition[0] > x and y + height > mousePosition[1] > y:
                if click[0] == 1 and action != None:
                    if action == "singleplayer":
                        #opens singleplayer
                        singleplayer_pong()
                    elif action == "multiplayer":
                        #opens multiplayer
                        multiplayer_pong()
                    elif action == "quit":
                        #quits game
                        pygame.quit()
                        quit()
        #menu buttons
        button(ballColour, 150, 190, 150, 50, "singleplayer")
        button(colourBlue, 150, 250, 150, 50, "multiplayer")
        button(colourRed, 150, 310, 150, 50, "quit")
        #updates menu
        pygame.display.flip()
        clock.tick(15)

def singleplayer_pong():
    #colours
    global colourRed
    global colourBlack
    global colourBlue
    global colourWhite
    global colourGreen
    global multi_ballColour
    #general variables
    global player1score
    global player2score
    global clock
    #reset score
    player1score = 0
    player2score = 0
    #paddle class
    class paddle(pygame.sprite.Sprite):
        def __init__(self, colour, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(colourBlack)
            self.image.set_colorkey(colourBlack)
            #draws paddle
            pygame.draw.rect(self.image, colour, [0, 0, width, height])
            self.rect = self.image.get_rect()
        def moveUp(self, pixels):
            self.rect.y -= pixels
            if self.rect.y < 0:
                self.rect.y = 0
        def moveDown(self, pixels):
            self.rect.y += pixels
            if self.rect.y > 400:
                self.rect.y = 400
    #ball class
    class Ball(pygame.sprite.Sprite):
        def __init__(self, colour, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(colourBlack)
            self.image.set_colorkey(colourBlack)
            #draws ball
            pygame.draw.rect(self.image, colour, [0, 0, width, height])
            self.vel = [randint(4, 8), randint(-8, 8)]
            self.rect = self.image.get_rect()
        def update(self):
            self.rect.x += self.vel[0]
            self.rect.y += self.vel[1]
        def bounce(self):
            self.vel[0] = -self.vel[0]
            self.vel[1] = randint (-8, 8)
    #setting up window
    gameWindow = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Pong")
    #paddle 1 settings
    paddle1 = paddle(colourRed, 10, 100)
    paddle1.rect.x = 20
    paddle1.rect.y = 200
    #paddle 2 settings
    paddle2 = paddle(colourBlue, 10, 100)
    paddle2.rect.x = 670
    paddle2.rect.y = 200
    #ball settings
    pongball = Ball(ballColour, 10, 10)
    pongball.rect.x = 350
    pongball.rect.y = 200
    #adds paddles withint sprite group
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(paddle1)
    all_sprites_list.add(paddle2)
    all_sprites_list.add(pongball)
    #AI fail functionality
    AIfailprob = 0.1
    #main loop
    runProgram = True
    while runProgram:
        #allowing closing of game through GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runProgram = False
        #keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.moveUp(10)
        if keys[pygame.K_s]:
            paddle1.moveDown(10)
        #AI paddle functionality
        if random.random() > AIfailprob:
            if pongball.rect.top < paddle2.rect.top:
                paddle2.moveUp(10)
            elif pongball.rect.bottom > paddle2.rect.bottom:
                paddle2.moveDown(10)
        else:
            paddle2.moveUp(10)
            paddle2.moveDown(0) 
        #ball functionality
        if pongball.rect.x >= 690:
            player1score += 1
            pongball.rect.x = 350
            pongball.rect.y = 200
        if pongball.rect.x <= 0:
            player2score += 1
            pongball.rect.x = 350
            pongball.rect.y = 200
        if pongball.rect.y > 490:
            pongball.vel[1] = -pongball.vel[1]
        if pongball.rect.y < 0:
            pongball.vel[1] = -pongball.vel[1]
        #paddle-ball collision
        if pygame.sprite.collide_mask(pongball, paddle1) or pygame.sprite.collide_mask(pongball, paddle2):
            pongball.bounce()
        #screen drawing
        gameWindow.fill(colourGreen)
        #draws net and linings
        pygame.draw.line(gameWindow, colourWhite, [350, 0], [350, 500], 5)
        pygame.draw.rect(gameWindow, colourWhite, [3, 20, 695, 455], 5)
        pygame.draw.circle(gameWindow, colourWhite, [350, 250], 30, 5)
        pygame.draw.circle(gameWindow, colourWhite, [350, 250], 80, 5)
        #draws other sprites
        all_sprites_list.draw(gameWindow)
        #game logic
        all_sprites_list.update()
        #display scores
        font = pygame.font.Font(None, 74)
        text = font.render(str(player1score) + " - " + str(player2score), 1, colourBlack)
        gameWindow.blit(text, (305, 10))
        pygame.display.flip()
        #FPS
        clock.tick(70)
#multiplayer_function
def multiplayer_pong():
    #colours
    global colourRed
    global colourBlack
    global colourBlue
    global colourWhite
    global colourGreen
    global multi_ballColour
    #general variables
    global player1score
    global player2score
    global clock
    #reset score
    player1score = 0
    player2score = 0
    #paddle class
    class paddle(pygame.sprite.Sprite):
        def __init__(self, colour, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(colourBlack)
            self.image.set_colorkey(colourBlack)
            #draws paddle
            pygame.draw.rect(self.image, colour, [0, 0, width, height])
            self.rect = self.image.get_rect()
        def moveUp(self, pixels):
            self.rect.y -= pixels
            if self.rect.y < 0:
                self.rect.y = 0
        def moveDown(self, pixels):
            self.rect.y += pixels
            if self.rect.y > 400:
                self.rect.y = 400
    #ball class
    class Ball(pygame.sprite.Sprite):
        def __init__(self, colour, width, height):
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(colourBlack)
            self.image.set_colorkey(colourBlack)
            #draws ball
            pygame.draw.rect(self.image, colour, [0, 0, width, height])
            self.vel = [randint(4, 8), randint(-8, 8)]
            self.rect = self.image.get_rect()
        def update(self):
            self.rect.x += self.vel[0]
            self.rect.y += self.vel[1]
        def bounce(self):
            self.vel[0] = -self.vel[0]
            self.vel[1] = randint (-8, 8)
    #paddle 1 settings
    paddle1 = paddle(colourRed, 10, 100)
    paddle1.rect.x = 20
    paddle1.rect.y = 200
    #paddle 2 settings
    paddle2 = paddle(colourBlue, 10, 100)
    paddle2.rect.x = 670
    paddle2.rect.y = 200
    #ball settings
    pongball = Ball(ballColour, 10, 10)
    pongball.rect.x = 350
    pongball.rect.y = 200
    #adds paddles withint sprite group
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(paddle1)
    all_sprites_list.add(paddle2)
    all_sprites_list.add(pongball)
    #main loop
    runProgram = True
    while runProgram:
        #allowing closing of game through GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runProgram = False
        #keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.moveUp(10)
        if keys[pygame.K_s]:
            paddle1.moveDown(10)
        if keys[pygame.K_UP]:
            paddle2.moveUp(10)
        if keys[pygame.K_DOWN]:
            paddle2.moveDown(10) 
        #ball functionality
        if pongball.rect.x >= 690:
            player1score += 1
            pongball.rect.x = 350
            pongball.rect.y = 200
        if pongball.rect.x <= 0:
            player2score += 1
            pongball.rect.x = 350
            pongball.rect.y = 200
        if pongball.rect.y > 490:
            pongball.vel[1] = -pongball.vel[1]
        if pongball.rect.y < 0:
            pongball.vel[1] = -pongball.vel[1]
        #paddle-ball collision
        if pygame.sprite.collide_mask(pongball, paddle1) or pygame.sprite.collide_mask(pongball, paddle2):
            pongball.bounce()
        #screen drawing
        gameWindow.fill(colourGreen)
        #draws net and linings
        pygame.draw.line(gameWindow, colourWhite, [350, 0], [350, 500], 5)
        pygame.draw.rect(gameWindow, colourWhite, [3, 20, 695, 455], 5)
        pygame.draw.circle(gameWindow, colourWhite, [350, 250], 30, 5)
        pygame.draw.circle(gameWindow, colourWhite, [350, 250], 80, 5)
        #draws other sprites
        all_sprites_list.draw(gameWindow)
        #game logic
        all_sprites_list.update()
        #display scores
        font = pygame.font.Font(None, 74)
        text = font.render(str(player1score) + " - " + str(player2score), 1, colourBlack)
        gameWindow.blit(text, (305, 10))
        pygame.display.flip()
        #FPS
        clock.tick(50)
#launches game
pong_menu()
#closes engine
pygame.quit()
