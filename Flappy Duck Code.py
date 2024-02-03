#Importing Modules to use in my code
from turtle import window_height, window_width
import pygame 
from pygame.locals import *
import random

#Initialises pygame so it can be used
pygame.init()

#Locks the game to a certain framerate
clock = pygame.time.Clock()
fps = 60

#Variables for Window
window_width = 1000
window_height = 600
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Flappy Duck")

#Variables for Game
scrolling_floor = 0
scrolling_speed = 3
birdStart = False
gameEnd = False
obstacle_spacing = pygame.time.get_ticks() - 2000
obstacle_timer = 1500
plane_speed = 5
shark_speed = 3
ball_speed_x = 4
ball_speed_y = 4
font = pygame.font.SysFont("ScoreFont.ttf", 50)
black = (0,0,0)
score = 0
score_spacing = pygame.time.get_ticks()
score_timer = 2000



#Load Images
background = pygame.image.load("background.png")
floor = pygame.image.load("floor.png")
menu = pygame.image.load("menu.png")
startButton = pygame.image.load("startbutton.png")
closeButton = pygame.image.load("closebutton.png")
restartButton = pygame.image.load("restartbutton.png")

#Starter Menu
def GameMenu():
   window.blit(menu,(0,0))
   start = Button(200,400, startButton)
   close = Button(650,400, closeButton)

   run = True
   while run:
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
        
         if start.draw() == True:
            Game()
         if close.draw() == True:
             pygame.quit()
         pygame.display.update()

#Button Class
class Button():
    def __init__(self,x,y,image):
        #Creates the button
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self):
        #Variable to Customise Result of button
        event = False
        #gets mouse position on the screen
        mousePosition = pygame.mouse.get_pos()
        #Condition to Activate Button
        if self.rect.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            event = True
        #Puts the button onto the screen
        window.blit(self.image, (self.rect.x,self.rect.y))

        return event
        

#Duck Class
class Duck(pygame.sprite.Sprite):
    #Initiliases the Class
    def __init__(self,xvalue,yvalue):
        pygame.sprite.Sprite.__init__(self)
        #List of all sprites related to animation
        self.animation = []
        #Index stores which item it is on the list
        self.index = 0
        #Counter counts when it needs to switch index
        self.counter = 0
        #Loads the ducks sprite in animation form
        for animation in range(1,5):
            #Loads the image currently used for animation
            ani_img = pygame.image.load(f"duck{animation}.png")
            #Makes the image suitable size/direction for the game
            ani_img = pygame.transform.scale(ani_img,(64,64))
            ani_img = pygame.transform.flip(ani_img,90,0)
            #Adds the image into the animation list
            self.animation.append(ani_img)
        #Finds which image to load in the list
        self.image = self.animation[self.index]
        #Creates a hitbox around the image
        self.rect = self.image.get_rect()
        #The center of the sprite
        self.rect.center = [xvalue, yvalue]
        self.velocity = 0
        self.mouseClick = False

    def update(self):
        #Counts up until anicd to switch image from the animation list
        self.counter += 1
        anicd = 8
        #Resets counter and goes to the next image in the list
        if self.counter > anicd:
            self.counter = 0
            self.index += 1
            #Once index reaches the end of the list resets it to the front
            if self.index >= len(self.animation):
                self.index = 0
        #Finds which image to load in the list
        self.image = self.animation[self.index]
        
        #End
        if duck.rect.bottom > 450:
           self.gameEnd = True
        
        #Gravity
        if birdStart == True:
           self.velocity += 2
           if self.velocity > 2:
               self.velocity = 2
           if self.rect.bottom < 450:
              self.rect.y  += self.velocity

        #Jump
        if gameEnd == False:
           if pygame.mouse.get_pressed()[0] == 1 and self.mouseClick == True:
               self.velocity = -15
               self.mouseClick = False
        #Prevents the mouse just being held
        if pygame.mouse.get_pressed()[0] == 0 and self.mouseClick == False:
            self.mouseClick = True
        #Sets Up a Roof
        if self.rect.top < 0:
            self.rect.y -= self.velocity
        
        #Left, Right Movement
        if gameEnd == False:
            #Left
            if pygame.key.get_pressed()[pygame.K_a]:
               self.rect.x -= 5
            if self.rect.left < 0:
               self.rect.x += 5
            #Right
            if pygame.key.get_pressed()[pygame.K_d]:
               self.rect.x += 5
            if self.rect.right > 1000:
               self.rect.x -= 5

#Obstacles Class
class Obstacle1(pygame.sprite.Sprite):
    #Initiliases the Class
    def __init__(self,xvalue,yvalue):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Obstacle1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [xvalue, yvalue]

    def update(self):
        self.rect.x -= plane_speed

class Obstacle2(pygame.sprite.Sprite):
    #Initiliases the Class
    def __init__(self,xvalue,yvalue):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Obstacle2.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [xvalue, yvalue]

    def update(self):
        self.rect.y -= shark_speed

class Obstacle3(pygame.sprite.Sprite):
    #Initiliases the Class
    def __init__(self,xvalue,yvalue):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Obstacle3.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [xvalue, yvalue]

    def update(self):
        global ball_speed_x,ball_speed_y
        self.rect.x -= ball_speed_x
        self.rect.y -= ball_speed_y
        if self.rect.top <= 0 or self.rect.bottom >= 500:
            ball_speed_y *= -1
                
#Sprite Groups
character_group = pygame.sprite.Group()
duck =  Duck(100,(window_height/2))
character_group.add(duck)
obstacle_group = pygame.sprite.Group()

#Draw Function
def draw():
    #Allows variables to be assigned/used outside function
    global scrolling_floor, scrolling_speed
    #Draws the images/sprites into the window
    window.blit(background, (0,0))
    window.blit(floor, (scrolling_floor,450))
    #Scrolling Background
    scrolling_floor -= scrolling_speed
    if abs(scrolling_floor) > 1000:
        scrolling_floor = 0
    #Draws the Sprites in the group
    character_group.draw(window)
    character_group.update()
    obstacle_group.draw(window)
    obstacle_group.update()
    Score_Counter()
    End()
    #Updates the window to show changes happening to the screen
    pygame.display.update()

#END GAME
def End():
    global gameEnd, score
    restart = Button(450,250, restartButton)
    if duck.rect.bottom >= 450:
        gameEnd = True
    if pygame.sprite.groupcollide(character_group,obstacle_group, False, False):
        gameEnd = True
    if gameEnd == True:
        if restart.draw() == 1:
            gameEnd = False
            score = Restart()

def Restart():
    global score, obstacle_timer, plane_speed, shark_speed, ball_speed_x, ball_speed_y
    obstacle_group.empty()
    duck.rect.x = 100
    duck.rect.y = window_height/2
    obstacle_timer = 1500
    plane_speed = 5
    shark_speed = 3
    ball_speed_x = 4
    ball_speed_y = 4
    score = 0
    return score
        
#Obstalce Generation
def generate():
    global gameEnd, birdStart, obstacle_timer, obstacle_spacing
    if gameEnd == False and birdStart == True:
        current = pygame.time.get_ticks()
        choice = random.randint(1,3)
        if choice == 1:
           if current - obstacle_timer > obstacle_spacing:
               obstacle1_Y = random.randint(0,350)
               obstacle1 = Obstacle1(1000,obstacle1_Y)
               obstacle_group.add(obstacle1)
               obstacle_spacing = pygame.time.get_ticks()
               choice = random.randint(1,3)
        if choice == 2:
            if current - obstacle_timer > obstacle_spacing:
               obstacle2_X = random.randint(200,800)
               obstacle2 = Obstacle2(obstacle2_X,450)
               obstacle_group.add(obstacle2)
               obstacle_spacing = pygame.time.get_ticks()
               choice = random.randint(1,3)
        if choice == 3:
            if current - obstacle_timer > obstacle_spacing:
               obstacle3_Y = random.randint(0,400)
               obstacle3 = Obstacle3(1000,obstacle3_Y)
               obstacle_group.add(obstacle3)
               obstacle_spacing = pygame.time.get_ticks()
               choice = random.randint(1,3)

#Score Counter
def Score_Counter():
    global score
    text= font.render("Score: "+str(score), False, black)
    window.blit(text, [450,485])

#Adds to the score counter
def Add_Score():
    global score, score_timer, score_spacing, gameEnd
    current = pygame.time.get_ticks()
    if current - score_timer > score_spacing and gameEnd == False :
        score += 1
        score_spacing = pygame.time.get_ticks()

#Events that occur when a certain score is reached
def Events():
    global score, plane_speed, shark_speed, ball_speed_x, ball_speed_y, obstacle_timer 
    choice = 0 
    if score != 0:
       if score%5 == 0:
           choice = random.randint(1,3)
    if choice == 1:
        obstacle_timer -= 250
    if choice == 2:
        plane_speed += 1
        shark_speed += 1
        ball_speed_x += 1
        ball_speed_y += 1
    if choice == 3:
        score += 1

#The Main Game Loop
def Game():
   global birdStart, gameEnd
   
   #Variable that decides if the game is on or off
   run = True
   #Game Loop
   while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and birdStart == False and gameEnd == False:
            birdStart = True
        if event.type == pygame.KEYDOWN and birdStart == False and gameEnd == False:
            birdStart = True
        

    draw()
    generate()
    Add_Score()
    End()
    Events()
    clock.tick(fps)

   pygame.quit()

#Main Code
GameMenu()