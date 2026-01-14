import pygame
import random

#initialize
pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 40) 
cockroachSize = 80



# Load and resize the image
try:
    cockroach = pygame.image.load('cockroach.png')
    cockroach = pygame.transform.scale(cockroach, (cockroachSize, cockroachSize))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

class Bar:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    #randomize y position
    def height(self):
        self.y = random.randint(240,400)
        
    #move left by 1
    def move(self):
        if (self.x <= -60):
            self.x = 750 
            self.height()
        self.x -= 1
    
    def draw_bar(self,i,j,k):
        #draw lower bar
        pygame.draw.rect(SCREEN, (i,j,k), (self.x, self.y, 60, 240))
        #draw upper bar
        pygame.draw.rect(SCREEN, (i,j,k), (self.x, self.y - 400, 60, 240))



class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocity = 0
    
    #make self jump (no update of self position in this function)
    def jump(self):
        self.velocity -= 7

    #make self fall (with update of self position)
    def update(self):
        #check upper boundary (as self size is define as 80, upper boundary = -size/2)
        if(self.y <= -40):
            self.y = -40
            self.velocity = 0

        #check lower boundary (as self size is define as 80, lower boundary = screen height + size/2) (screen size = 400)
        elif(self.y >= 440):
            self.y = 440
            self.velocity = 0

        #change velocity and update self position 
        else:
            self.velocity += 0.25
            self.y += self.velocity

    #update self on screen
    def draw(self):
        SCREEN.blit(cockroach, (self.x, self.y))


class Text:
    def __init__(self):
        self.x = cockroachSize/4
        self.y = cockroachSize/4
        self.n = 0        # n = current score of the player

    #increse score by 1
    def change(self):
        self.n+=1

    #reset score
    def reset(self):
        self.n = 0

    #update score
    def draw(self,i,j,k):
        text = font.render("Score: "+ str(self.n), True, (i,j,k))
        SCREEN.blit(text, (self.x,self.y))


def touches(player,bar):
    #if player touches bars or the boundaries, 3*cockroachSize/4 and cockroachSize/4 are variable added to adjust effective intersections of the bars and the player
    if (player.x >= bar.x-3*cockroachSize/4 and player.x <= bar.x+60+cockroachSize/4 and 
        ((player.y >= bar.y-3*cockroachSize/4 and player.y <= bar.y+240) or
        (player.y >= bar.y-400 and player.y <= bar.y-160-cockroachSize/4))):
        return True
    return False
    

      


def gamestart(player, bar1, bar2, bar3):

    #reset player
    player.x = 200
    player.y = 200

    #reset bars
    bar1.x = 640 
    bar1.y = 240    #Bar(640, 240)
    bar2.x = 910
    bar2.y = 40     #Bar(910, 40)
    bar3.x = 1180
    bar3.y = 40     #Bar(1180, 40)


def main ():

    #define status of the game
    start = False
    end = False

    #create player
    player = Player(200, 200)
    player.velocity = 0

    #create bars
    bar1 = Bar(640, 240)
    bar2 = Bar(910, 40)
    bar3 = Bar(1180, 40)

    #create text
    text = Text()

    #colors
    i=255
    j=0
    k=0


    while True:

        for event in pygame.event.get():

            #check status of the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #check key press(space)
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    #firse key press start the game
                    if (end):
                        end = False
                        gamestart(player,bar1,bar2,bar3)
                    else:
                        if (not start and not end):
                            bar1.height()
                            bar1.draw_bar(k,i,j)
                            bar2.height()
                            bar2.draw_bar(k,i,j)
                            bar3.height()
                            bar3.draw_bar(k,i,j)
                            start = True
                    if (start and not end):
                        player.jump()        
        
        
        #check whether player touches bars
        if (touches(player,bar1) or touches(player,bar2) or touches(player,bar3) or player.y >= 440 or player.y <= -40):
            if (not end):
                player.velocity = 0
                end = True
                start = False
                text.reset()

        #check whether player get a score
        if (player.x == bar1.x or player.x == bar2.x or player.x == bar3.x):
            text.change()

        #make the player fall after first key press
        if (start and not end):
            player.update()
            bar1.move()
            bar2.move()
            bar3.move()

        # Clear screen
        SCREEN.fill((i,j,k))

        if (i == 255 and j< 255 and k == 0):
            j += 1
        elif (i > 0 and j == 255 and k == 0):
            i -= 1
        elif (i == 0 and j == 255 and k< 255):
            k += 1
        elif (i == 0 and j > 0 and k == 255):
            j -= 1
        elif (i < 255 and j == 0 and k == 255):
            i += 1
        elif (i == 255 and j == 0 and k > 0):
            k -= 1

        #draw bars
        bar1.draw_bar(k,i,j)
        bar2.draw_bar(k,i,j)
        bar3.draw_bar(k,i,j)
        
        #draw player
        player.draw()

        #draw text
        text.draw(j,k,i)

        # Update display ONCE per frame
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()



