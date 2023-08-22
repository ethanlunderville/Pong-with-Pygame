import pygame
from pygame import mixer
import time
import random
from constants import *
from sys import exit

class Player(pygame.sprite.Sprite):

    # Note: The incrementScore and getScore score methods are class methods because there
    # will only ever be one instance of each. Although I could have just referenced the 
    # names of the instances of the objects in the Circle class when updating the score 
    # I instead chose to make the score a classmember as I felt that this was better design 

    score = 0
    player_paddle = pygame.Surface((20, 200))
    #Draws player
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,120])
        self.image.fill('White')
        self.rect = self.image.get_rect(center = (25,300))
        pygame.draw.rect(self.image, 'White', self.rect)
    #Creates Mouse Based Movement
    def update(self):
            mousex, mousey = pygame.mouse.get_pos()
            self.rect.y = mousey - 100

    @classmethod
    def incrementScore(self):
        self.score += 1

    @classmethod
    def getScore(self):
        return self.score

    def getRect(self):
        return self.rect
    
class Circ(pygame.sprite.Sprite):
    # resets the x val
    resval = 16
    xval = 16
    slope = .6
    #Adjusts the extremeness of the change in slope of the line the ball follows by adding a random number
    #Between 0 and the volatility
    volatility = BALL_VOLATILITY
    ## Y cord of the ball is sent to the Computer Player in order for it to adjust its position
    ycord = 0
    #Draws The Ball
    def __init__(self):
        super().__init__()
        self.inititializeBall()
    
    def inititializeBall(self):
        self.size = BALL_SIZE
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill('Black')
        self.image.set_colorkey('Black')
        pygame.draw.circle(self.image, 'White', (self.size // 2, self.size // 2), self.size // 2)
        #500,20
        self.rect = self.image.get_rect(center=(500,20))

    #Animates the ball
    def collide(self):
        if self.rect.colliderect(player.rect) and self.rect.left>=31 or self.rect.colliderect(robot.rect) and self.rect.right <=969 :
            # Changes direction of the ball with a new slope that has some RNG so that
            # the game is not overly deterministic
            self.slope = -self.slope + random.randint(1, self.volatility) * .01
            self.xval = -self.xval
            # in the case that the ball collides with the player and it is set on a path in which
            # it will score on the computer player without touching either of the top or bottom bounds
            # this updates where the bot should go by changing the ycord value
            if self.rect.colliderect(player) and self.slope != 0:
                    xfar = SCREEN_WIDTH - self.rect.centerx
                    self.ycord = - ((xfar * self.slope)-self.rect.centery)-15
                    
    def update(self):
        self.yval = self.xval * self.slope
        #if the ball touches either the lower or upper bounds
        if self.rect.y >= SCREEN_HEIGHT or self.rect.y <= 0:
            # Changes the trajectory of the ball
            if self.slope > 0:
                self.slope = -self.slope + random.randint(1,self.volatility)*.01
            else:
                self.slope = -self.slope - random.randint(1,self.volatility)*.01                                   
            self.yval = -self.yval
            # Updates yval for computer player
            if self.rect.y >= SCREEN_HEIGHT:
                xfar = SCREEN_WIDTH - self.rect.centerx
                self.ycord = SCREEN_HEIGHT - (xfar * self.slope)
            elif self.rect.y<=0:
                xfar = SCREEN_WIDTH - self.rect.centerx
                self.ycord = - (xfar * self.slope)
        #these two conditons decide what the ball does when either player scores
        elif self.rect.x >= SCREEN_WIDTH:
            self.xval = self.resval
            self.yval = 0
            #redraws at the start
            self.inititializeBall()
            Player.incrementScore()
            self.slope = .6
            time.sleep(1)
        elif self.rect.x <= 0:
            self.xval = -self.resval
            self.yval = 0
            # redraws at the start
            self.inititializeBall()
            Robot.incrementScore()
            self.slope = .6
            time.sleep(1)
        ## Animates the ball based off of the conditions above
        self.rect.x += self.xval
        self.rect.y += -self.yval

    def getRect(self):
        return self.rect
    
class Robot(Player):
    score = 0
    # draws computer player
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,120])
        self.image.fill('White')
        self.rect = self.image.get_rect(center = (975,300))
        self.score = 0
        pygame.draw.rect(self.image, 'Red', self.rect)

    def update(self, circle):
            # Prevents computer player from going off the stage
            if self.rect.centery >= 600:
                self.rect.centery -= 1
                pass
            elif self.rect.centery <= 65:
                self.rect.centery += 1
                pass
            #Make the computer player try to chase the ball based on the y cord
            elif circle.ycord < self.rect.centery:
                if (self.rect.centery - circle.ycord) < 5:
                    self.rect.centery -= 1
                else:
                    self.rect.centery -= 10
            elif circle.ycord > self.rect.centery:
                if circle.ycord - self.rect.centery < 5:
                    self.rect.centery += 1
                else:
                    self.rect.centery += 10

#General
pygame.init()
#1000, 650
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("PONG")
surf = pygame.Surface((1,1))
surf.fill('White')
pygame.display.set_icon(surf)
clock = pygame.time.Clock()
#Scores
font = pygame.font.Font(None, 50)
#Backround
background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
#line going down the middle
surface2 = pygame.Surface((1,SCREEN_HEIGHT))
surface2.fill('White')
#Both paddles and the ball
circ = Circ()
player = Player()
robot = Robot()
#Sprite list
sprites = pygame.sprite.Group()
sprites_list = pygame.sprite.Group()
sprites_list.add(player)
sprites_list.add(circ)
sprites_list.add(robot)
paused = False 

while 1>0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
    if not paused:
        screen.blit(background, (0, 0))
        # Draws sprites added to the sprite list
        sprites_list.draw(screen)
        # Draws line down the middle
        screen.blit(surface2, (500, 0))
        # Draws The Scores
        player_one_score = font.render(str(Player.getScore()), True, 'White')
        player_two_score = font.render(str(Robot.getScore()), True, 'White')
        screen.blit(player_one_score, (450, 20))
        screen.blit(player_two_score, (532, 20))
        # Animates circle
        Circ.update(circ)
        # Mouse functionality
        player.update()
        # Robot
        robot.update(circ)
        #Handle Collisons
        if circ.getRect().colliderect(player.getRect()) and circ.getRect().left>=31 or circ.getRect().colliderect(robot.getRect()) and circ.getRect().right <=969 :
            circ.collide()
        # General
        pygame.display.update()
        clock.tick(CLOCK_RATE)


