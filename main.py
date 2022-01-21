import pygame
from pygame import mixer
import time
import random
from sys import exit

class Player(pygame.sprite.Sprite):
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
class Circ(pygame.sprite.Sprite):
    player_paddle = pygame.Surface((20, 200))
    # resets the x val
    resval = 16
    xval = resval
    yval = 0
    slope = .6
    #Adjusts the extremeness of the change in slope of the line the ball follows by adding a random number
    #Between 0 and the volatility
    volatility = 40

    p1_score_val = 0
    p2_score_val = 0
    ## Y cord of the ball is sent to the Computer Player in order for it to adjust its position
    ycord = 0

    #Draws The Ball
    def __init__(self):
        size = 10
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill('Black')
        self.image.set_colorkey('Black')

        pygame.draw.circle(self.image, 'White', (size // 2, size // 2), 5)
        #500,20
        self.rect = self.image.get_rect(center=(500,20))

    #Animates the ball
    def update1(self):
        self.yval = self.xval * self.slope
        ## if the ball touches the player or the robot

        # The two comparisons are to prevent the ball from going back and fourth superfast within the paddle when the
        # robot or player hit with either the top or bottom of their paddles
        if self.rect.colliderect(player.rect) and self.rect.left>=31 or self.rect.colliderect(robot) and self.rect.right <=969 :
            #print("player right: " + str(player.rect.right))
            #print("Ball left: " + str(self.rect.left))

            #print("Their sum" + str(self.rect.left > player.rect.right))
            print("robot left: " + str(robot.rect.left))
            print("Ball right: " + str(self.rect.right) )

            # sound

            impact.play()
            #Changes direction of the ball with a new slope that has some RNG so that
            # the game is not overly deterministic


            self.slope = -self.slope + random.randint(1, self.volatility)*.01
            self.xval = -self.xval

                # in the case that the ball collides with the player and it is set on a path in which
                # it will score on the computer player without touching either of the top or bottom bounds
                # this updates where the bot should go by changing the ycord value

            if self.rect.colliderect(player) and self.slope != 0:
                    xfar = 1000 - self.rect.centerx
                    self.ycord = -((xfar * self.slope)-self.rect.centery)-15

        #if the ball touches either the lower or upper bounds
        elif self.rect.y >= 650 or self.rect.y <= 0:
            # sound
            impact.play()
            # Changes the trajectory of the ball
            self.slope = -self.slope - random.randint(1,self.volatility)*.01
            self.yval = -self.yval
            # Updates yval for computer player
            if self.rect.y >= 650:
                xfar = 1000 - self.rect.centerx
                self.ycord = 650 - (xfar * self.slope)

            elif self.rect.y<=0:
                xfar = 1000 - self.rect.centerx
                self.ycord = - (xfar * self.slope)
        #these two conditons decide what the ball does when either player scores
        elif self.rect.x >= 1000:
            self.xval = self.resval
            self.yval = 0
            #redraws at the start
            self.__init__()
            self.p1_score_val += 1
            self.slope = .6

            time.sleep(1)
            # Spawn noise
            spawn.play()

        elif self.rect.x <= 0:
            self.xval = -self.resval
            self.yval = 0
            # redraws at the start
            self.__init__()
            self.p2_score_val += 1
            self.slope = .6

            time.sleep(1)
            # Spawn noise
            spawn.play()
        ## Animates the ball based off of the conditions above
        self.rect.x += self.xval
        self.rect.y += -self.yval
class Robot(pygame.sprite.Sprite):
    # draws computer player
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,120])
        self.image.fill('White')
        self.rect = self.image.get_rect(center = (975,300))

        pygame.draw.rect(self.image, 'Red', self.rect)

    def update(self):
            # Prevents computer player from going off the stage
            if self.rect.centery >= 600:
                self.rect.centery -= 1
                pass
            elif self.rect.centery <= 65:
                self.rect.centery += 1
                pass
            #Make the computer player try to chase the ball based on the y cord
            elif circ.ycord < self.rect.centery:
                if (self.rect.centery - circ.ycord) < 5:
                    self.rect.centery -= 1
                else:
                    self.rect.centery -= 10
            elif circ.ycord > self.rect.centery:
                if circ.ycord - self.rect.centery < 5:
                    self.rect.centery += 1
                else:
                    self.rect.centery += 10


#General
pygame.init()
#Sounds
spawn = mixer.Sound('NewGen.wav')
spawn.set_volume(.25)

impact = mixer.Sound('Impact.wav')
impact.set_volume(.13)
#1000, 650
screen = pygame.display.set_mode((1000,650))
pygame.display.set_caption("PONG")
surf = pygame.Surface((1,1))
surf.fill('White')
pygame.display.set_icon(surf)
clock = pygame.time.Clock()
#Scores
font = pygame.font.Font(None, 50)
#Backround
background = pygame.Surface((1000,650))
#line going down the middle
surface2 = pygame.Surface((1,700))
surface2.fill('White')
#Both paddles and the ball
player = Player()
circ = Circ()
robot = Robot()
#Sprite list
sprites = pygame.sprite.Group()
sprites_list = pygame.sprite.Group()

sprites_list.add(player)
sprites_list.add(circ)
sprites_list.add(robot)

while 1>0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    # Draws sprites added to the sprite list
    sprites_list.draw(screen)
    # Draws line down the middle
    screen.blit(surface2, (500, 0))
    # Draws The Scores
    player_one_score = font.render(str(circ.p1_score_val), True, 'White')
    player_two_score = font.render(str(circ.p2_score_val), True, 'White')
    screen.blit(player_one_score, (450, 20))
    screen.blit(player_two_score, (532, 20))
    # Animates circle
    Circ.update1(circ)
    # Mouse functionality
    player.update()
    # Robot
    robot.update()
    # General
    pygame.display.update()
    clock.tick(60)


